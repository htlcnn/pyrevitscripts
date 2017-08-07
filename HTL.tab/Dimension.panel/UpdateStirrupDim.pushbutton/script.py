# -*- coding: utf-8 -*-
__title__ = 'Update\nStirrup Dim'
__author__ = 'htl'
import rpw

dims = rpw.db.Collector(of_category='Dimensions',
                        where=lambda x: 'udic stirrup' in x.Name.lower())

def update_below_text(dim, segment=None):
    spacing_text = 'Ø' + dim.Name.split(' - ')[-1]
    spacing = int(spacing_text.split('a')[-1])
    with rpw.db.Transaction('update stirrup dim'):
        if not segment:
            number = int(float(dim.ValueString)/spacing)
            dim.Below = str(number) + spacing_text
        else:
            number = int(float(segment.ValueString)/spacing)
            segment.Below = str(number) + spacing_text

for dim in dims:
    if dim.NumberOfSegments > 0:
        for segment in dim.Segments:
            update_below_text(dim, segment)
    else:
        update_below_text(dim)
