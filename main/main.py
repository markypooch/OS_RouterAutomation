############################################################################
#
# Demo       -           OpenStack Neutron Router Creation
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#
# Revision 1 - 8/18/17 - Created GUI for form emulation, and created
#                        object for Neutron Router. Calls to API for
#                        creation of Router. Configurable Router Name,
#                        and Tenant ID, and Router ID
#
#############################################################################

######## Imports ########
from Tkinter      import *
from openstack    import connection
from openstack    import session
from NetworkTypes import Neutron_Router
from GUIClasses   import RouterInterfaceWindow
#########################

######## Globals ########
#########################
# Yes, we all know they are bad practice, but this is only a demo app, do as I say, not as I do :D
# python  makes the syntax more explicit. Each time they are referenced in local scope, the global keyword
# will precede it
radioButtons               = []
entry                      = []
frames                     = []
neutronRouterPointerObject = None
routerIntWin               = None
conn                       = None
nrp                        = None
choice                     = None
root                       = None
imgLabel                   = None
#########################

###########################################################
#
#   function  - displayRouterInformationToDialog
#   arguments - TopLevel TKinter GUI Handle, NeutronRouterPointer
#   purpose   - displays router information to top-level gui dialog
#   returns   - void
#
###########################################################
def displayRouterInformationToDialog(topLevel, nrp):
    if nrp is None:
        raise AssertionError("Neutron Router Pointer is nullptr")

    labelName        = Label(topLevel, text=nrp.name)
    labelName.pack()
    labelTenantID    = Label(topLevel, text=nrp.status)
    labelTenantID.pack()
    labelBasePath    = Label(topLevel, text=nrp.base_path)
    labelBasePath.pack()
    labelID          = Label(topLevel, text=nrp.id)
    labelID.pack()
    return

###########################################################
#
#   function  - createRouter, deleteRouter, and getRouter
#   arguments - none
#   Purpose   - createRouter - makes a call to the neutronRouterObject, and retrieves pointer to
#                              new Neutron Router.
#               deleteRouter - with a valid pointer to a neutron router, attempt to remove it
#                              from the OpenStack environment
#               getRouter    - retrieve a pre-existing neutron router
#   returns   - void
#
###########################################################
def createRouter():
    global nrp
    nrp                 = neutronRouterPointerObject.createNewNeutronRouter()

    topLevel            = Toplevel()
    topLevel.title("Created")
    topLevel.iconbitmap('ibm.ico')

    labelTitle          = Label(topLevel, text="Created New Router")
    labelTitle.pack()

    displayRouterInformationToDialog(topLevel, nrp)
    return


def deleteRouter():
    topLevel            = Toplevel()
    topLevel.title("Deleted")
    topLevel.iconbitmap('ibm.ico')

    labelTitle          = Label(topLevel, text="Deleted Router")
    labelTitle.pack()

    global nrp
    displayRouterInformationToDialog(topLevel, nrp)
    nrp = neutronRouterPointerObject.deleteNeutronRouter()
    return


def getRouter():
    global nrp
    nrp                 = neutronRouterPointerObject.getNeutronRouter(entry[0].get())

    topLevel            = Toplevel()
    topLevel.title("Get")
    topLevel.iconbitmap('ibm.ico')
    labelTitle          = Label(topLevel, text="Retrieved Router")
    labelTitle.pack()

    displayRouterInformationToDialog(topLevel, nrp)
    return

### CALLBACK ###############################################
############################################################
#
#   function  - onButtonRouterIntClicked
#   arguments - handle to event
#   purpose   - create new instance of RouterInterfaceWindow
#               to manage, and encapsulate the functionality
#               of the child window
#   returns   - void
#
############################################################
def onButtonRouterIntClicked(event):
    global routerIntWin
    global nrp


    routerIntWin = RouterInterfaceWindow.RouterInterfaceWindow(neutronRouterPointerObject)
    routerIntWin.createGUI()
    return

### CALLBACK ###############################################
############################################################
#
#   function  - onButtonExecuteClicked
#   arguments - handle to event
#   purpose   - instantate neutronRouterObject if nullptr
#               perform switch-case depending on radiobutton
#               checked (createNewRouter, getRouter, deleteRouter
#   return    - void
#
############################################################
def onButtonExecuteClicked(event):
    global neutronRouterPointerObject
    global entry
    if neutronRouterPointerObject is None:
        neutronRouterPointerObject = Neutron_Router.Neutron_Router(conn,
                                                                   entry[0].get(),
                                                                   entry[1].get(),
                                                                   entry[2].get())


    radButtonOptions = {
        1: createRouter,
        2: deleteRouter,
        3: getRouter,
    }

    global choice
    radButtonOptions[choice.get()]()

##################################################
#
#   function  - entrypoint
#   arguments - none
#   purpose   - Our entrypoint. Main GUI logic goes here (root frame)
#               and the calls for the root form widget callbacks are
#               made here
#   returns   - void
#
##################################################
def entrypoint():

    global root

    # Root frame creation, and set GUI size
    root         = Tk()
    root.geometry("700x160")
    root.title("Openstack Router Automation")

    # Choice intege r for radiobutton selection
    global choice
    choice = IntVar()
    choice.set(1)

    canvas = Canvas(root)
    photo = PhotoImage(file='./oslogo.gif')

    canvas.create_image(50, 50, image=photo)
    canvas.place(x=0, y=0)

    # Main Label for GUI, and Array members for widget creation

    routerOptions = [
        "Create New Router       ",
        "Delete Router           ",
        "Get Existing Router Info",
    ]
    routerParameters = [
        "Router Name:",
        "Router ID:",
        "Tenant ID:",
    ]

    # Populate our Our Form
    for i in range(0, 3, 1):
        # Append the radio buttons in a linear top down fashion
        radioButtons.append(Radiobutton(
            root,
            text=routerOptions[i],
            padx=20,
            variable=choice,
            value=i+1,
        ))
        radioButtons[i].place(x=120, y=(i*30)+5)

        # Add the radioButtons in a linear top down fashion, append the entry labels,
        # during the last iteration of the loop
        if i == 2:
            for j in range(0, 3, 1):
                Label(root, text=routerParameters[j]).place(x=350, y=(j*30)+5)
                entry.append(Entry(root))
                entry[j].place(x=510, y=(j*30)+5)

    buttonInterfaces = Button(root, text="Configure Router Interfaces...")
    buttonInterfaces.place(x=350, y=120)
    buttonInterfaces.bind('<Button-1>', onButtonRouterIntClicked)


    # Create the execution button
    buttonExecute = Button(root, text="Perform OpenStack Operation")
    buttonExecute.place(x=140, y=120)

    # Associate our callback method to the button
    buttonExecute.bind('<Button-1>', onButtonExecuteClicked)

    # Get our handle to the API by authenticating against KeyStoneAuth
    global conn
    conn = connection.Connection(auth_url='https://10.0.147.13:5000/v3',
                                 project_name='admin',
                                 username='<USER NAME>',
                                 password='<PASSWORD>',
                                 user_domain_id='default',
                                 project_domain_id='default')

    root.iconbitmap('ibm.ico')
    root.resizable(0, 0)

    # Call the GUI framework for mainloop functionality (Message Pumps/Input Capture)
    mainloop()

######### ENTRY POINT ##########
entrypoint()
