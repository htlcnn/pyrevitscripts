# -*- coding: utf-8 -*-
__title__ = 'Without Number'
__author__ = 'htl'
import rpw

dims = rpw.db.Collector(of_category='Dimensions',
                        where=lambda x: 'udic stirrup' in x.Name.lower(),
                        view=rpw.doc.ActiveView)

delete_dims = rpw.db.Collector(of_category='Dimensions',
                        where=lambda x: 'udic stirrup' not in x.Name.lower(),
                        view=rpw.doc.ActiveView)

def update_below_text(dim, segment=None):
    spacing_text = 'Ø' + dim.Name.split(' - ')[-1]
    spacing = int(spacing_text.split('a')[-1])
    with rpw.db.Transaction('Update Stirrup Dim'):
        if not segment:
            dim.Below = spacing_text
        else:
            segment.Below = spacing_text

def delete_below_text(dim, segment=None):
    with rpw.db.Transaction('Delete Below Text'):
        if not segment:
            dim.Below = ''
        else:
             segment.Below = ''

for delete_dim in delete_dims:
    if delete_dim.NumberOfSegments > 0:
        for segment in delete_dim.Segments:
            delete_below_text(delete_dim, segment)
    else:
        delete_below_text(delete_dim)

for dim in dims:
    if dim.NumberOfSegments > 0:
        for segment in dim.Segments:
            update_below_text(dim, segment)
    else:
        update_below_text(dim)
