"""
events2pdf:  create on demand pdf event schedule 

Copyright (C) 2023 C. Wayne Davis
Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.
This software is provided "as is" and the author disclaims all warranties with regard to this software including all implied warranties of merchantability and fitness. In no event shall the author be liable for any special, direct, indirect, or consequential damages or any damages whatsoever resulting from loss of use, data or profits, whether in an action of contract, negligence or other tortious action, arising out of or in connection with the use or performance of this software.

DEPENDENCIES:
Python 3.6 or above
Reportlab
Pyinstaller manages all

INSTALLATION:
See docs/README.install

INPUTS:
config file: contains defaults, below, allowing config changes without changing this script

input file: json list of dicts, each dict contains 1 event's info, filename is in config file or defaults below if config file not found,

if command line arg -i xxx is given, input filename will be xxx.  If xxx is '-', stdin will be used

OUTPUTS:
pdf file, name specified in config file, defaults below or on command line option' -o xxx' or '-o -' for stdout
"""

CONFIG_FILE = "../resources/events2pdf_conf.json"
DEBUG=False

# if config file not found
mdefaults = {
		"mevents_url":				"https://aagainesville.org/wp-admin/admin-ajax.php?action=meetings",
		"minput":						"../resources/events.json", 
		"moutput":					"../events2pdf.pdf",
		"mtypes":						[ "in_person",  "hybrid"],
		"mpage_size":				"legal",
		"mpage_orientation":	"landscape",
        "mcols":						3,
		"mcol_widths":				[0.17, 0.62, 0.21],
        "mframe_count":	  		4,
        "mfont":						"Helvetica",
        "mfont_bold":        	   "Helvetica-Bold",
        "mfont_size":				8,
		"mleading":					1.1,
        "mpage_margin":			0.5,
		"mcover_page":			"../resources/coverpage.jpg",
		"mcover_page_size":	0.7,
		"msection":			    	["SUNDAY",
											"MONDAY",
											"TUESDAY",
											"WEDNESDAY",
											"THURSDAY",
											"FRIDAY",
											"SATURDAY"
											]
}		

from reportlab.lib.pagesizes import legal, letter, landscape, portrait
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, Table, TableStyle, PageTemplate, KeepTogether, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch

import  os, sys, json, re, logging

def log(level, msg):
   # log = logging.getLogger("xhtml2pdf")
    print(f"level: {level}  {msg}", file=sys.stderr)
    
from reportlab.lib import utils      

def get_image(path, width):        # image is cover page
    img = utils.ImageReader(path)
    iw, ih = img.getSize()               # shrinks image to fit frame
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect)) 
    
# functions to format column data for rows
    
def format_col0(m):
    return(m['time_formatted'])
               
def format_col1(m):          # format event name, address, notes
    maddr = re.match('(.*)\s'+m['region'], m['formatted_address'])[1].rstrip(', ')
    maddr = re.sub('[ -]', '&nbsp;', maddr)
    if 'notes' in m:
        maddr += f"<br/>{m['notes']}" 
    return( f"<b>{m['name']}</b><br/>{m['location']},  {maddr}")

def format_col2(m):
    return(f"<b>{m['region']}</b>")   

def get_events(conf, events):
    global DEBUG
    if (DEBUG): print(f"GET_EVENTS: {len(events)} events at entry", file=sys.stderr)
    if (DEBUG): print(f"GET_EVENTS: events[0] =  {events[0]}", file=sys.stderr)
    styles = getSampleStyleSheet()
    styleM = ParagraphStyle('events',
                           fontName = conf['mfont'],
                           fontSize=conf['mfont_size'],
                           parent=styles['Normal'], 
                           leading=conf['mfont_size']*conf['mleading'],
                           alignment= TA_LEFT)
                           
    styleD = ParagraphStyle('headings',
                           fontName = conf['mfont_bold'],
                           fontSize=conf['mfont_size'] + 3,
                           parent=styles['Normal'],
                           alignment= TA_CENTER,
                           keepWithNext = 1)    

    try:                              #  get event types specified in config
        events =  [x for x in events if x['attendance_option'] in conf['mtypes']]  
    except Exception as err:
        log(logging.CRITICAL, f"failure filtering event types: {err}")
        return ([])
        
    msection = []                       # split events into lists by sections
    for d in range(len(conf['msection'])):
       msection.append([x for x in events if x['day'] == d])
       
    data = []
    try:                        # add section headings then all events for each section
        for i in range(len(msection)):              # add heading row
            p = Paragraph(f"<b>{conf['msection'][i]}</b><br/>" , styleD)
            p.keepWithNext = True
            data.append([None, p])                       # put heading in second column
            
            for m in msection[i]:                                  # format event    
                data.append([                # currently 3 columns per table row
                    Paragraph(format_col0(m), styleM),
                    Paragraph(format_col1(m), styleM),
                    Paragraph(format_col2(m), styleM)
                ])

    except Exception as err:
        log(logging.CRITICAL,  f"failure formatting event: {m}\n{err}")
        return ([])          
        
    return(data)
    
import events2pdf_cover_page  as CP
from datetime import datetime
def show_events(conf, data):
    if DEBUG: print(f"SHOW_EVENTS: len data = {len(data)}", file=sys.stderr)
 
    if conf['mpage_size'] == 'letter':
         pagesize = letter
    elif conf['mpage_size'] == 'legal':     
        pagesize = legal
    else:
        log(logging.WARNING, f"unknown pagesize: {conf['mpage_size']}, using legal")
        pagesize =legal
        
    if conf['mpage_orientation'] == 'landscape':
        pagesize = [pagesize[1], pagesize[0]]
        
    if conf['moutput'] == '-':
        mout = sys.stdout.buffer
    else:
        mout =  conf['moutput']

    doc = BaseDocTemplate(
                    mout,
                    pagesize=pagesize,
                    leftMargin = conf['mpage_margin']*inch,
                    rightMargin = conf['mpage_margin']*inch,
                    topMargin = conf['mpage_margin']*inch,
                    bottomMargin = conf['mpage_margin']*inch,  
                    allowSplitting=1,
                    showBoundary=0                      # change to 1 to see frame outlines
                    )
  
    tablestyle =  TableStyle([
            ('TOPPADDING', (0,0),(-1,-1), 0),     
            ('BOTTOMPADDING', (0,0),(-1,-1), 2),
            ('LEFTPADDING', (0,0),(-1,-1), 0),
            ('RIGHTPADDING', (0,0),(-1,-1),3),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ])                  

    styles = getSampleStyleSheet()
    styleCP = ParagraphStyle('cover_page',
               fontName = conf['mfont'],
               fontSize=conf['mfont_size'],
               parent=styles['Normal'],
               leading=conf['mfont_size']*1.4,
               alignment= TA_CENTER)
    
    frameCount = conf['mframe_count']
    frameWidth = doc.width / frameCount
    frameHeight = doc.height
    
    frames = []                     #construct frames
    try:
        for frame in range(frameCount):   
            leftMargin = doc.leftMargin + frame*frameWidth
            column = Frame(leftMargin, doc.bottomMargin, frameWidth, frameHeight)
            frames.append(column)
    except Exception as err:
        log(logging.CRITICAL, "can't build pdf frames")
        return(-1)
         
    template = PageTemplate(id = None, frames=frames)
    doc.addPageTemplates(template) 

    elements = []  
    t_date = datetime.now().strftime("%m/%d/%Y")   
    elements.append(Paragraph(f"{t_date}<br/>",  styleCP)) 
    
    try:                        # get cover page
        if os.path.exists(conf['mcover_page']):         # shrink image to fit frame
            img = get_image(conf['mcover_page'], frameWidth*conf['mcover_page_size'])
            elements.append(img)
        else:
            mcover_page = CP.make_cover_page()
            elements.append(Paragraph(mcover_page,  styleCP)) 
    except Exception as err:            
        log(logging.WARNING, "can't get cover page")
        
    cw = []
    try:
        for x in conf['mcol_widths']:
            cw.append(x*frameWidth) 
        t = Table(data, cw)                      
        t.setStyle(tablestyle)
        elements.append(t)
        doc.build(elements) 
    except Exception as err:            
        log(logging.CRITICAL, "can't build pdf")
        return(-1)
        
    return(0)
    
    
""" Doesn't work, security?
import requests
# url to get json events dump
events_url = "https://aagainesville.org/wp-admin/admin-ajax.php?action=events"
events =  json.loads(requests.get(events_url).text)
 requests.get(events_url).text
'<head><title>Not Acceptable!</title></head><body><h1>Not Acceptable!</h1><p>An appropriate representation of the requested resource could not be found on this server. This error was generated by Mod_Security.</p></body></html>'
"""
 
import io
def main():
    global DEBUG

    # resource paths are relative to script home, not cwd
    # pyinstaller changes __file__ so can't use that
    os.chdir(os.path.dirname(sys.argv[0]))
    
    conf = get_config()
    if conf is None or len(conf) == 0:
        log(logging.CRITICAL, f"get config failed")
        sys.exit(-1) 
        
    if DEBUG: print(f"MAIN: got conf {len(conf)}", file=sys.stderr)   
    
    try:    
        if conf['minput'] == '-':      # strip BOM
            if DEBUG: print(f"MAIN: using stdin", file=sys.stderr)
            stdin_wrapper = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8-sig')
            events = json.load(stdin_wrapper)
            if DEBUG: print(f"MAIN: got {len(events)} from stdin", file=sys.stderr)
        else:
            if DEBUG: print(f"MAIN: using {conf['minput']}", file=sys.stderr)
            try:
                with open(conf['minput'], "r") as f:
                    events = json.load(f)
                    if DEBUG: print(
                        f"MAIN: got {len(events)} from {conf['minput']}", file=sys .stderr)                 
            except FileNotFoundError as err:
                log(logging.CRITICAL, f"failed to get input from {conf['minput']}: {err}")
                sys.exit(-1)
    except Exception as err:
         log(logging.CRITICAL, f"failed to get events from stdin: {err}")
         sys.exit(-1)   
        
    data = get_events(conf, events)
    if len(data) > 0:
        r = show_events(conf, data)
        if r == 0:
            sys.exit(0)
            
    sys.exit(-1)
    
import getopt
def get_config():
    try:                            # load config from file or use defaults if no config file
        conf = json.load(open(CONFIG_FILE))
    except FileNotFoundError as err:
        conf = mdefaults
        log(logging.WARNING,
            f"error loading config file {CONFIG_FILE}, using defaults: {err}")
    except Exception as err:
        log(logging.CRITICAL, f"fatal error loading config file {CONFIG_FILE}: {err}")
        return([]) 
        
    # override defaults with any command line args
    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"i:o:f:b:s:hlp")
        except Exception as err:
            print(f"invalid options: { sys.argv[1:]} getopt returned {err}", file=sys.stderr)
            usage()
            return([])
          
        for opt, arg in opts:
            if opt in ['-i']:
                conf['minput'] = arg
            elif opt in ['-o']:
                conf['moutput']  = arg
            elif opt in ['-f']:
                conf['mfont'] = arg
            elif opt in ['-b']:
               conf['mfont_bold'] = arg    
            elif opt in ['-s']:
               conf['mfont_size'] = arg
            elif opt in ['-h']:
                usage()
                return(-1)
            elif opt in ['-p']:
                conf['mpage_size'] = 'portrait'
            elif opt in   ['-l']:
                conf['mpage_orientation'] = 'letter'    
                
    if DEBUG:
        print(f"GET_COFIG: returning:", file=sys.stderr)    
        for k, v in conf.items():
            print (k, v)            
    return(conf)

def usage():
    print(f"usage: defaults will be used for missing arguments\n",
              f"-[h] print this message and exit\n",
              f"-[i] input_file | -, - means stdin\n",
              f"-[o] output_file | -, - means stdout\n",
              f"-[f] fontname, ex, 'Arial'\n",
              f"-[b] bold_font_name, ex, 'Arial-Bold'\n",
              f"-[s] font_size in points\n",
              f"-[p] page orientation: portrait, default is landscape\n",
              f"-[l] page size: letter, default is legal", file=sys.stderr)          
   
if __name__ == '__main__':
    main()