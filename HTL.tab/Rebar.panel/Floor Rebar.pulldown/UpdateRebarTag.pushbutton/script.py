# -*- coding: utf-8 -*-
__title__ = 'Update Floor\nRebar Tag'
__author__ = 'htl'
import rpw
from rpw import doc

rebar_details = rpw.db.Collector(of_class='FamilyInstance',
                        where=lambda x: x.Symbol.FamilyName.lower()=='udic - floor rebar symbol',
                        view = doc.ActiveView)
with rpw.db.Transaction('Update Floor Rebar Detail'):
    for detail in rebar_details:
        detail = rpw.db.Element(detail)
        rebar_id = int(detail.parameters['Rebar ID'].AsString())
        rebar = rpw.db.Element.from_int(rebar_id)
        schedule_mark = rebar.ScheduleMark
        spacing = int(round(rebar.MaxSpacing * 304.8))
        rebar_type = rpw.db.Element.from_id(rebar.GetTypeId())
        diameter = int(round(rebar_type.BarDiameter * 304.8, 0))
        spacing_text = '{}a{}'.format(diameter, spacing)
        detail.parameters['Rebar ID'] = rebar_id
        detail.parameters['Rebar Schedule Mark'] = schedule_mark
        detail.parameters['Rebar Spacing'] = spacing_text
