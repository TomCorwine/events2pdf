#Copyright (C) 2023 Wayne Davis, cwaynedavis@gmail.com
#see LICENSE for license details
__doc__="""
events2pdf:  create a pdf event schedule

See ./docs/Installation
        ./docs/Configuration
        ./docs/README
        ./docs/README-Reportlab
"""

from reportlab.lib.pagesizes import legal, letter, landscape, portrait
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph,\
    Table, TableStyle, PageTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch

import  os, sys, json, re

try:
    import pyphen
except Exception as err:
   print(f"events2pdf: warning: hypenation will not work: {err}", file=sys.stderr)

CONFIG_FILE = "events2pdf_conf.json"

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='events2pdf.log',  filemode='w', level=logging.DEBUG)

def usage():
    print(f"usage: defaults will be used for missing arguments\n",
              f"[-h] print this message and exit\n",
              f"[-i] url | input_file | -, - means stdin\n",
              f"[-o] output_file | -, - means stdout\n",
              f"[-c] use this config file\n",
              f"[-f] fontname, ex, 'Helvetica'\n",
              f"[-s] font_size in points\n",
              f"[-p] page orientation: portrait, default is landscape\n",
              f"[-l] page size: letter, default is legal",
              file=sys.stderr)


import io
import requests

def load_events(arg):
    """Get events from stdin, url or file"""

    headers = {
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    try:
        if arg == '-':
            stdin_wrapper = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8-sig')
            events = json.load(stdin_wrapper)
        elif arg.find('http') >= 0:
            events =  json.loads(requests.get(arg, headers=headers).text)
        else:               # assume file
            with open(arg, "r") as f:
                events = (json.load(f))
    except Exception as err:
        logger.error( f"load_events: fatal error loading events from {arg}: {err}")
        return([])
    return(events)


import getopt

def get_config():
    """Parse command line args, get other args from config file."""

    c = {}
    config_file = CONFIG_FILE

    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"i:o:c:f:b:s:dhlp")
            for opt, arg in opts:
                logger.debug(f"get_config: opt = {opt}, arg={arg}")
        except Exception as err:
            print(f"invalid options: { sys.argv[1:]} {err}", file=sys.stderr)
            usage()
            return([])

        for opt, arg in opts:
            if opt in ['-i']:
                c['minput'] = arg
            elif opt in ['-o']:
                c['moutput']  = arg
            elif opt in ['-c']:
                config_file = arg
            elif opt in ['-f']:
                c['mfont'] = arg
            elif opt in ['-b']:
               c['mfont'] = arg
            elif opt in ['-s']:
               c['mfont_size'] = float(arg)
            elif opt in ['-h']:
                usage()
                return([])
            elif opt in ['-p']:
                c['mpage_size'] = 'letter'
            elif opt in   ['-l']:
                c['mpage_orientation'] = 'portrait'

    try:
        conf = json.load(open(config_file))
    except Exception as err:
        logger.error(f"get_config: fatal error loading config file {config_file}: {err}")
        return([])


    for k in c:			# override defaults or config file with any command line args
        conf[k] = c[k]

    return(conf)


import filetype

def is_image(f):
    """test if file is image"""

    ft = filetype.guess(f)
    if ft and ft.mime.find('image') >= 0:
        return(True)
    return(False)


from reportlab.lib import utils

def get_image(path, width):
    """Resize cover page image to fit frame."""

    try:
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return(Image(path, width=width, height=(width * aspect)))
    except Exception as err:
        logger.error(f"get_image: failed: {err}")
        return(None)


from datetime import datetime

def get_cover_page(conf, width):
    """Prepares cover page from image, text file or default in this script."""

    styles = getSampleStyleSheet()
    styleCP = ParagraphStyle('cover_page',
               fontName = conf['mfont'],
               fontSize=conf['mfont_size'],
               parent=styles['Normal'],
               leading=conf['mfont_size']*1.2,
               hyphenationLang = 'en',
               alignment= TA_CENTER)

    cp = []
    t_date = datetime.now().strftime("%m/%d/%Y")
    cp.append(Paragraph(f"<b>{t_date}</b>",  styleCP))

    if os.path.exists(conf['mcover_page']):
        if is_image(conf['mcover_page']):         # resize to fit frame
            img = get_image(conf['mcover_page'], width)
            if img:                             # just skip if get_image fails
                cp.append(img)
        else:
            try:
                with open(conf['mcover_page'], "r") as f:
                    cp.append(Paragraph(f.read(),  styleCP))
            except Exception as err:
                logger.error(f"get_cover_page: can't get cover page from file: {conf['mcover_page']}\n{err}")
                return(cp)
    else:
        logger.error(f"get_cover_page: using default cover page, file not found: {conf['mcover_page']}")
        cp.append(Paragraph(DEFAULT_COVER_PAGE,  styleCP))
    return(cp)

"""
functions to format table cells
format_group() re explanation:
  capture address up to region name, strip trailing comma or space
  re.match('(.*)\s'+m['region'], m['formatted_address'])[1].rstrip(', ')
  formatted_address = '17405 US-441, High Springs, FL 32643, USA'
  region = 'High Springs'
  captured address = '17405 US-441'
"""

def format_time(m):
    return(m['time_formatted'])

def group_name(m):
    """Format group name and designations."""

    designations_map = {
        'O': 'O',
        'C': 'C',
        'D': 'D',
        'MED': 'M',
        'SP': 'S',
        'B': 'BB',
        'LIT': 'LIT',
        'ST': 'SS',
        'BE': 'BG',
        'CF': 'CF',
        'X': 'WC',
    }

    designations = []
    for key, value in designations_map.items():
        if key in m['types']:
            designations.append(value)

    return f"{m['name']} {'/'.join(designations)}"

def format_group(m):
    """Format event name, address, notes."""

    maddr = re.match('(.*)\s'+m['region'], m['formatted_address'])[1].rstrip(', ')
    maddr = re.sub('[ -]', '&nbsp;', maddr)         # make maddr non breaking
    if 'notes' in m:
        maddr += f"<br/>{m['notes']}"
    return( f"<b>{group_name(m)}</b><br/>{m['location']}, {maddr}")

def format_region(m):
    return(f"<b>{m['region']}</b>")

def get_events(conf, events):
    """Get events, format them for table."""

    logger.debug(f"get_events: {len(events)} events at entry")
    logger.debug(f"get_events: events[0] =  {events[0]}")

    styles = getSampleStyleSheet()
    styleE = ParagraphStyle('events',
        fontName = conf['mfont'],
        fontSize= conf['mfont_size'],
        parent = styles['Normal'],
        leading = conf['mfont_size']*conf['mleading'],
        wordWrap = 'LTR',
        hyphenationLang = 'en',
        alignment = TA_LEFT
    )

    try:              #  select event types specified in config
        events = [x for x in events if x['attendance_option'] in conf['mtypes']]
    except Exception as err:
        logger.error(f"get_events: failure filtering event types: {err}")
        return ([])

    sections = []
    logger.debug(f"len conf['msections'] = {len(conf['msections'])}")
    try:                # split events into lists by sections
        for s in range(len(conf['msections'])):
            sections.append([x for x in events if x['day'] == s])
    except Exception as err:
        logger.error(f"get_events: failure splitting events by section: {err}")
        return ([])

    fmt_sections = []
    try:
        for i in range(len(sections)):
            data = []
            for e in sections[i]:         # format event
                data.append([
                    Paragraph(format_time(e), styleE),
                    Paragraph(format_group(e), styleE),
                    Paragraph(format_region(e), styleE)
                ])
            fmt_sections.append(data)

    except Exception as err:
        logger.error(f"get_events: failure formatting events: {err}\n{err}")
        return ([])

    return(fmt_sections)

def show_events(conf, sections):
    """Create pdf, frames, table, add events."""

    logger.debug(f"show_events: len sections = {len(sections)}")

    if conf['mpage_size'] == 'letter':
         pagesize = letter
    elif conf['mpage_size'] == 'legal':
        pagesize = legal
    else:
        logger.error(f"show_events: unknown pagesize: {conf['mpage_size']}, using legal")
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
        showBoundary=0                      # 1 to see frame outlines
    )

    styles = getSampleStyleSheet()
    tablestyle =  TableStyle([
        ('TOPPADDING', (0,0),(-1,-1), 0),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ('LEFTPADDING', (0,0),(-1,-1), 0),
        ('RIGHTPADDING', (0,0),(-1,-1),3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])

    styleH = ParagraphStyle('headings',
        fontName = conf['mfont'],
        fontSize=conf['mfont_size'] + 3,
        parent=styles['Normal'],
        alignment= TA_CENTER,
        hyphenationLang = 'en',
        keepWithNext = 1
    )

    frame_count = conf['mframe_count']
    frame_width = doc.width / frame_count
    frame_height = doc.height

    logger.debug(f"show_events: fc = {frame_count}, fw = {frame_width}, fh = {frame_height}")

    frames = []                     #construct frames
    try:
        for f in range(frame_count):
            leftMargin = doc.leftMargin + f * frame_width
            column = Frame(leftMargin, doc.bottomMargin, frame_width, frame_height)
            frames.append(column)
    except Exception as err:
        logger.error("show_events: can't build pdf frames: {err}")
        return(-1)

    template = PageTemplate(id = None, frames=frames)
    doc.addPageTemplates(template)

    col_widths = []

    for x in conf['mcol_widths']:
        col_widths.append((int(x)/100)*frame_width)

    # initialize elements list with cover page
    elements = get_cover_page(conf, frame_width)

    """
    add section heading styled keepWithNext, then table with 1 row
    for keepWithNext to bind to, finally add table of remaining rows of section
    """
    try:
        for i in range(len(sections)):
            elements.append(Paragraph(f"<b>{conf['msections'][i]}</b>" , styleH))  # heading cwd
            t = Table([sections[i].pop(0)], col_widths)     # 1 row table
            t.setStyle(tablestyle)
            elements.append(t)

            t = Table(sections[i], col_widths)
            t.setStyle(tablestyle)
            elements.append(t)

        doc.build(elements)
    except Exception as err:
        logger.error( f"show_events: can't build pdf: {err}")
        return(-1)

    return(0)

def events2pdf_sub(conf):
    """Called as sub"""

    r = do_events(conf)
    if r == 0:
       logger.info(f"created pdf file  {conf['moutput']}")

def main():
    """Create pdf list of events."""

    conf = get_config()
    if conf is None or len(conf) == 0:
        logger.error(f"main: can't get config")
        sys.exit(-1)
    r = do_events(conf)
    if r == 0:
       logger.info(f"created pdf file  {conf['moutput']}")

def do_events(conf):

    try:
        events = load_events(conf['minput'])
        if events is None or len(events) == 0:
            raise Exception("got 0 events")
    except Exception as err:
         logger.error(f"main: failed to get events from {conf['minput']}: {err}")
         return(-1)

    sections = get_events(conf, events)
    if len(sections) > 0:
        show_events(conf, sections)
        return(0)


if __name__ == '__main__':
    main()




