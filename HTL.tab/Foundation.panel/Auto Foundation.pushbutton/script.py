# -*- coding: utf-8 -*-
import clr
import rpw
from rpw.ui.forms import Button, ComboBox, FlexForm, CheckBox, Label, TextBox, Separator
from rpw import doc
import os


clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import SaveAsOptions, Transaction, IFamilyLoadOptions

def get_family_parameter_value(familydoc, name):
    famman = familydoc.FamilyManager
    for p in famman.Parameters:
        if p.Definition.Name == name:
            return famman.CurrentType.AsValueString(p)

def set_family_parameter_value(familydoc, param, value):
    famman = familydoc.FamilyManager
    with rpw.db.Transaction('Set parameter', doc=familydoc):
        famman.Set(param, value)


def get_family_parameter(familydoc, name):
    famman = familydoc.FamilyManager
    for p in famman.Parameters:
        if p.Definition.Name == name:
            return p

def associate_family_parameter(doc, nested_instance, param_name):
    nested_param = nested_instance.LookupParameter(param_name)
    for p in doc.FamilyManager.GetParameters():
        if p.Definition.Name == param_name:
            host_param = p
    with rpw.db.Transaction('Associate parameter {}'.format(param_name), doc=doc):
        doc.FamilyManager.AssociateElementParameterToFamilyParameter(nested_param, host_param)

def main():
    pile_width = int(ff.values['pile_width'])
    piles_along_length = int(ff.values['piles_along_length'])
    piles_along_width = int(ff.values['piles_along_width'])
    pile_spacing_along_length = float(ff.values['pile_spacing_along_length'])
    pile_spacing_along_width = float(ff.values['pile_spacing_along_width'])
    length_cover = float(ff.values['length_cover'])
    width_cover = float(ff.values['width_cover'])
    thickness = float(ff.values['thickness'])
    pile_cutoff = float(ff.values['pile_cutoff'])

    foundation = rpw.db.Element.from_id(ff.values['foundation_id'])
    pile = rpw.db.Element.from_id(ff.values['pile_id'])
    foundation_famdoc = doc.EditFamily(foundation.unwrap())
    pile_famdoc = doc.EditFamily(pile.unwrap())

    saveas_path = os.path.expanduser('~')
    save_options = SaveAsOptions()
    save_options.OverwriteExistingFile = True

    pile_famdoc.SaveAs(os.path.join(saveas_path, '{}'.format(pile_famdoc.Title)), save_options)

    with rpw.db.Transaction('Load pile into foundation', doc=foundation_famdoc):
        foundation_famdoc.LoadFamily(pile_famdoc.PathName)

    pile_famdoc.Close(False)

    with rpw.db.Transaction('Activate pile family symbol', doc=foundation_famdoc):
        pile_family_symbol = rpw.db.Collector(of_class='FamilySymbol',
                                              doc=foundation_famdoc,
                                              where=lambda x: x.FamilyName==pile.Name)[0]
        # http://thebuildingcoder.typepad.com/blog/2014/08/activate-your-family-symbol-before-using-it.html
        if not pile_family_symbol.IsActive:
            pile_family_symbol.Activate()

    ### Place piles
    first_x = -pile_spacing_along_length*(piles_along_length-1)/2
    first_y = -pile_spacing_along_width*(piles_along_width-1)/2
    z = pile_cutoff - thickness
    pile_locations = []
    for i in range(piles_along_length):
        for j in range(piles_along_width):
            x = first_x + i * pile_spacing_along_length
            y = first_y + j * pile_spacing_along_width
            pile_locations.append((x, y, z))
    with rpw.db.Transaction('Insert pile instances', doc=foundation_famdoc):
        for x, y, z in pile_locations:
            x = x / 304.8
            y = y / 304.8
            z = z / 304.8
            foundation_famdoc.FamilyCreate.NewFamilyInstance(rpw.DB.XYZ(x,y,z),
                                                            pile_family_symbol,
                                                            rpw.DB.Structure.StructuralType.NonStructural)

    created_piles = list(rpw.db.Collector(of_category='OST_StructuralFoundation',
                                        of_class='FamilyInstance',
                                        doc=foundation_famdoc))
    parameters = ['Number of pile segments', 'D', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7']
    for pile in created_piles:
        for param_name in parameters:
            associate_family_parameter(foundation_famdoc, pile, param_name)


    length_param = get_family_parameter(foundation_famdoc, 'Length')
    width_param = get_family_parameter(foundation_famdoc, 'Width')
    thickness_param = get_family_parameter(foundation_famdoc, 'Foundation Thickness')
    length = pile_spacing_along_length*(piles_along_length-1) + 2 * length_cover
    width = pile_spacing_along_length*(piles_along_width-1) + 2 * width_cover
    set_family_parameter_value(foundation_famdoc, length_param, length / 304.8)
    set_family_parameter_value(foundation_famdoc, width_param, width / 304.8)
    set_family_parameter_value(foundation_famdoc, thickness_param, thickness / 304.8)
    set_family_parameter_value(foundation_famdoc, get_family_parameter(foundation_famdoc, 'D'), pile_width/304.8)

    new_filename = ff.values['new_foundation_family_name'] or 'new_{}'.format(foundation_famdoc.Title)
    foundation_famdoc.SaveAs(os.path.join(saveas_path, '{}.rfa'.format(new_filename)),
                            save_options)
    foundation_rfa_path = foundation_famdoc.PathName
    foundation_famdoc.Close(False)

    rpw.ui.forms.Alert('Finished creating foundation, saved at {}'.format(foundation_rfa_path))
    os.startfile(foundation_rfa_path)




foundations = rpw.db.Collector(of_class='Family',
                               where=lambda x: x.FamilyCategory.Name=='Structural Foundations')

components = [Label('Select Pile Cap:'),
            ComboBox('foundation_id', {f.Name: f.Id for f in foundations}),
            Label('Select Rectangular Pile:'),
            ComboBox('pile_id', {f.Name: f.Id for f in foundations}),
            Label('Pile width (D):'),
            TextBox('pile_width'),
            Label('Number of piles along Length:'),
            TextBox('piles_along_length'),
            Label('Number of piles along Width:'),
            TextBox('piles_along_width'),
            Label('Pile spacing along Length:'),
            TextBox('pile_spacing_along_length'),
            Label('Pile spacing along Width:'),
            TextBox('pile_spacing_along_width'),
            Label('Length cover:'),
            TextBox('length_cover'),
            Label('Width cover:'),
            TextBox('width_cover'),
            Label('Foundation Thickness:'),
            TextBox('thickness'),
            Label('Pile Cut-off:'),
            TextBox('pile_cutoff'),
            Label('New Foundation Family Name:'),
            TextBox('new_foundation_family_name'),
            Separator(),
            Button('Create foundation')]

ff = FlexForm("Modify Structural Foundation Family", components)
ff.show()

if ff.values:
    main()
