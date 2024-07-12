# **events2pdf README**

The python script **events2pdf** extracts meeting info and creates a meeting table.  The pdf page to be created is divided into vertical frames and the meeting table is inserted frame by frame with new pages created as needed.  Pdf layout is set in the config file so it can be altered without changing the script.

The current config is landscape, legal; font Helvetica 8 point.  This produces a 2 page pdf file.  With Helvetica 8 point, a legal, landscape pdf printed with 'scale to fit page' produces a usable letter size print.  This is convenient for anyone with no legal size paper.

**CONFIGURATION**:

The **configuration file**/events2pdf_conf.json**” specifies the format for the pdf file allowing pdf format changes without changing the python script.  See “**./docs/Configuration**” for info.  The command line option "**-c xxx**" specifies that the config file "**xxx**" is to be used.  "**-c -**" specifies using the default config in the script. If config file is specified but not found, fatal error.  A json config file is used for simplicity since no user will be changing the config file.

**COMMAND LINE ARGUMENTS**:

Command line arguments override config settings.

[-h] print usage message and exit
[-i] input_file | -, - means stdin (dash o space dash)
[-o] output_file | -, - means stdout 
[-c] config_file - use this config file
[-f] font_name, ex, 'Arial'
[-b] bold_font_name, ex, 'Arial-Bold'
[-s] font_size in points
[-p] page orientation: portrait, default is landscape
[-l] page size: letter, default is legal
[-d] turn on debugging prints to stderr

**INPUTS:** 

**event data** - a json list of dicts, from stdin, a file or  url.  Each event dict contains 1 event's info. The  input file name is set in config or with command line option "-i xxx". " -i -" (dash i space dash) input is stdin.

One event’s json entry is:
{"id":3542,"**name**":"**The Way Out  C\/STS\/WC**","slug":"the-way-out-c-sts-wc","updated":"2022-07-15 16:30:02","location_id":3423,"url":"https:\/\/aagainesville.org\/meetings\/the-way-out-c-sts-wc\/","**day**":**0**,"time":"07:30","end_time":"08:30","**time_formatted**":"**7:30 am**","edit_url":"https:\/\/aagainesville.org\/wp-admin\/post.php?post=3542&action=edit","types":["12x12","C","ST","X"],"**location**":"**First United Methodist Church**","location_url":"https:\/\/aagainesville.org\/locations\/first-united-methodist-church\/","**formatted_address**":"**17405 US-441, High Springs, FL 32643, USA**","approximate":"no","latitude":29.816205599999999975580067257396876811981201171875,"longitude":-82.5704414000000070927853812463581562042236328125,"region_id":70,"**region**":"**High Springs**","regions":["High Springs"],"**attendance_option**":"**in_person**"}

Text in bold are the key, value pairs used for the pdf event listings.

**OUTPUTS:** 

pdf file, name specified in config or on command line option "-o xxx" or "-o -" for stdout.

Sample **pdf output**, a 3 column row for one frame is:

​				SUNDAY
7:30 am		The Way Out C/STS/WC			High
​			First United Methodist Church,	Springs
​			17405 US 441

**error and debug output** to events2pdf.log.

**NOTES**:

Source dependencies are Python 3.7 or above, reportlab.

Note:  Added 'import filetype' to detect image files, moved to Ubuntu, ran pyinstaller, did not notice any errors or warnings but running executable failed, can't find module filetype.  Did pip install filetype.

The open source Reportlab Toolkit is used for pdf creation. The file “**./doc/README_Reportlab**” provides some information.  See https://docs.reportlab.com/ for more information.  Note that Reportlab Plus is a commercial package, this script only uses the free ReportLab PDF Toolkit.

Pyinstaller is used to package the script into a single executable. **events2pdf** can be run without installing a Python interpreter or any modules (**-c -** required in this case). **events2pdf** expects to find it's config file and the cover page in **./resources** .  If the cover page is not found, default text in the script will be used.  If the config file is not found and **"-c -"** not given the script will abort.

Two files are provided for the cover page:  **coverpage.png** and **coverpage.html**. Any text or image file can be used for the cover page, see **./docs/Configuration.** Image files will be resized to fit the frame. 

**coverpage.html** is interpreted by reportlab so only limited XML markup is allowed, see https://docs.reportlab.com/reportlab/userguide/ch6_paragraphs/#paragraph-xml-markup-tags “**Intra-paragraph markup**”.

Page size, orientation, fonts, cell spacing and number of frames per page can be changed in the config file to alter the pdf format.  The number of columns per event in the frame can also be changed but the script would have to be modified for this to work.

If the script doesn't create the desired number of pages in the pdf file, adjust the font and font size.  Other settings may be adjusted but one change may require other changes to produce decent output.  Improper changes can cause overwriting or hidden text.

