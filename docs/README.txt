The python script events2pdf extracts meeting info and creates a meeting table.  The pdf page to be created is divided into 4 vertical frames and the meeting table is inserted frame by frame with new pages created as needed.  Pdf layout is set in the config file so it can be altered without changing the script.
Input is json meeting list from stdin, file or possibly url although that isn't implemented at present.one meeting’s json entry is:
{"id":3542,"name":"The Way Out  C\/STS\/WC","slug":"the-way-out-c-sts-wc","updated":"2022-07-15 16:30:02","location_id":3423,"url":"https:\/\/aagainesville.org\/meetings\/the-way-out-c-sts-wc\/","day":0,"time":"07:30","end_time":"08:30","time_formatted":"7:30 am","edit_url":"https:\/\/aagainesville.org\/wp-admin\/post.php?post=3542&action=edit","types":["12x12","C","ST","X"],"location":"First United Methodist Church","location_url":"https:\/\/aagainesville.org\/locations\/first-united-methodist-church\/","formatted_address":"17405 US-441, High Springs, FL 32643, USA","approximate":"no","latitude":29.816205599999999975580067257396876811981201171875,"longitude":-82.5704414000000070927853812463581562042236328125,"region_id":70,"region":"High Springs","regions":["High Springs"],"attendance_option":"in_person"}
Text in bold are the key, values pairs used for the pdf event listings.

The configuration file “events2pdf_conf” in ~/resources specifies the format for the pdf file.  See “README_config.txt” for info.  If the configuration file is missing defaults in the script will be used, unless overridden by command line options.

The open source Reportlab Toolkit is used for pdf creation. The file “reportlab README.txt” provides some information.  See https://docs.reportlab.com/ for more information.  Note that Reportlab Plus is a commercial package, this script only uses the free ReportLab PDF Toolkit.

Pyinstaller is used to package the script into a single executable.  events2pdf expects to find it's config file and the cover page in ~/resources but defaults will be used if they're not found.

Command line arguments override the config file settings.  See the to be written man page.

The cover page for the pdf file will be  ~/resources/coverpage.jpg, if that image is missing the script will generate a text only cover page, see src/ events2pdf_cover_page.py.  This py script is bundled into the executable by pyinstaller so if changed pyinstaller must be run to see the new page. src/events2pdf_cover_page.py is interpreted by reportlab so only limited XML markup is allowed, see https://docs.reportlab.com/reportlab/userguide/ch6_paragraphs/#paragraph-xml-markup-tags “Intra-paragraph markup”.

