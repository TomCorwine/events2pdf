Configuration File

The script configuration is a dict in a json file: events_conf.json.  If you change the file be sure not to change the format, i.e. [...] is a python list, deleting the [ or ] will break the script.  All strings must be in double quotes, fractions must have a digit before the decimal point.  Deleting an entry will cause a python key error.

If the script doesn't create the desired number of pages in the pdf file, adjust the font and font size.  Other settings may be adjusted but note that one change may require other changes to produce decent output.  Improper changes can cause overwriting or hidden text.

Dict keys:

"m_url": link to get input, currently not implemented.

"minput": json input file with events, - for stdin or full pathname if not in resources directory.

"moutput": - for stdout or name for output pdf file.

"mtypes": [ "in_person",  "hybrid"]
These are the event types to be included.  Currently, types are "in_person",  "hybrid" and online.

"mpage_size": "legal"
legal or letter; legal = 8.5" x 14", letter = 8.5 x 11

"mpage_orientation": "landscape"
landscape or portrait

"mcols": 3
The number of columns per meeting row, currently 'time', 'name/address', region.

"mcol_widths": [0.17, 0.62, 0.21],
Column widths (percent) for each frame giving the column spacing within the frame.  Trailing widths may be omitted and remaining space will be divided equally.

"mframe_count":	4
4 frames per page, if this is changed spacing will be adjusted to fit.

"mfont": "Times-Roman"
Font name to be used.  A font not known to the reportlab library used by the script will not work, an alternate will be used. Reportlab  standard fonts are Helvetica, Courier, Times Roman. Additional fonts can be added on request.

"mfont_bold": "Times-Bold"
See above.

"mfont_size":	8
Size in points.

"mleading":	1.2
Specifies space between lines in a paragraph.  1.2 means spacing is 20% of line.  Less than 1 and text will be overwritten.  Higher spacing means fewer lines will fit on a page.

"mpage_margin":	0.5
Outer page margin in inches

"mcover_page":	image file name
Image to use for cover page, blank or file not found - canned text cover will be used.  See src/events2pdf_cover_page.py but any changes won’t take effect until pyinstaller run again.

"mheadings":	["SUNDAY", ...]
Days of week, etc.




		
		
