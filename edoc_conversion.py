import os
import sys
import traceback

os.environ['PYSCRIPT_LOG_ENV'] = 'DEBUG'
print(os.environ['PYSCRIPT_LOG_ENV'])

import pyuno
import uno
from com.sun.star.beans import PropertyValue
from unohelper import Base, systemPathToFileUrl, absolutize
from com.sun.star.uno import Exception as UnoException, RuntimeException
from com.sun.star.connection import NoConnectException
from com.sun.star.lang import IllegalArgumentException
from com.sun.star.io import IOException

export_format = "writer_pdf_Export"
export_extension = "pdf"


def usage():
    print """Usage: %s in_file out_file
    You must start the office with this line before starting
    this script:
    soffice "-accept=socket,host=localhost,port=2002;urp;"
    """ % (os.path.basename(sys.argv[0]))


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    print in_path
    print out_path

    url = "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
    context = uno.getComponentContext()
    smgr = context.ServiceManager
    resolver = smgr.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", context)
    ctx = resolver.resolve(url)

    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

    in_props = PropertyValue()
    in_props.Name = "Hidden"
    in_props.Value = True
    file_url = systemPathToFileUrl(os.path.realpath(in_path))
    try:
        doc = desktop.loadComponentFromURL(file_url, "_blank", 0, tuple([in_props]))


        out_props = [PropertyValue() for i in range(2)]
        out_props[0].Name = "Overwrite"
        out_props[0].Value = True
        out_props[1].Name = "FilterName"
        out_props[1].Value = export_format

        out_url = systemPathToFileUrl(out_path)
        doc.storeToURL(out_url, tuple(out_props))
        doc.dispose()

    except AttributeError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        sys.exit(1)

    except NoConnectException, e:
        sys.stderr.write("OpenOffice process not found or not listening (" + e.Message + ")\n")
        sys.exit(1)

    except IllegalArgumentException, e:
        sys.stderr.write("The url is invalid ( " + e.Message + ")\n")
        sys.exit(1)

    except RuntimeException, e:
        sys.stderr.write("An unknown error occured: " + e.Message + "\n")
        usage()
        sys.exit(1)


if __name__ == "__main__":
    main()


