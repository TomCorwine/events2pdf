# Configuration

**Configuration** **File**

Configuration options can be overridden with command line options.

The script configuration is a dict in a json file: **events2pdf_conf.json**.  If you change the file be sure not to change the format, i.e. **[...]** is a python list, deleting the **[** or **]** will break the script.  All strings must be in double quotes, fractions must have a digit before the decimal point.  Deleting an entry will cause a python keyerror.

Page size, orientation, fonts, cell spacing and number of frames per page can be changed to alter the pdf format.  The number of columns per event in the frame can also be changed in the config file but the script would have to be modified for this to work.

If the script doesn't create the desired number of pages in the pdf file, adjust the font and font size.  Other settings may be adjusted but one change may require other changes to produce decent output.  Improper changes can cause overwriting or hidden text.

**Config Dict keys:**

**minput**: events source - must be json dict

**"-"** for stdin | url | file path.

**moutput**: output pdf file name or **"-"** for stdout.

**mtypes**: **[ "in_person", "hybrid"]**

These are the event types to be included. Currently, types are "in_person",  "hybrid" and "online".

**mpage_size**: **legal**

legal or letter; legal = 8.5" x 14", letter = 8.5 x 11, default legal

**mpage_orientation**: **landscape**

landscape or portrait, default landscape

**mcols**: **3**

Number of columns per meeting row, currently 'time', 'name/address', region.

**mcol_widths**: **[17, 62, 21]**

Column widths in percent for each frame giving the column spacing within the frame.  Trailing widths may be omitted and remaining space will be divided equally.

**mframe_count**: **4**

4 frames per page, if this is changed spacing will be adjusted to fit.

**mfont**: **"Helvetica"**

Font name to be used.  A font not known to the reportlab library used by the script will not work, an alternate will be used. 

**mfonts**:

List of standard fonts supported by Adobe PDF.

**mfont_size**: **8**

Size in points.

**mleading**: **1.1**

Space between lines in a paragraph.  1.1 means spacing is 10% of line.  Less than 1 and text will be overwritten.  Higher spacing means fewer lines will fit on a page.

**mpage_margin**:  **0.4**

Outer page margin in inches

**mcover_page**:  file name for cover page, any image format, html or text.

Image or html file to use for cover page. Image files will be resized to fit the frame. Html or text files may use only simple XML markup, see **./docs/README.md**. 

**mheadings**: **["SUNDAY", ...]**

Section Headings, days of week, etc.

 

 

 

 

​                    

​                    