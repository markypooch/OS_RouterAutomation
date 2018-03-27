from Tkinter import *

class RouterInterfaceWindow:
    neutronRouterPointer = None
    topLevelGUI          = None
    buttonCreateInt      = None
    buttonDeleteInt      = None
    radioBtnsList        = []
    interfaces           = []
    labelsList           = []
    entryList            = []
    radBtnChoice         = None

    labelText = [
        "Network Name:",
        "Subnet  Name:",
        "Port    Name:",
        "Tenant  ID:",
        "IPv4 Gateway:",
        "IPv4 Prefix:",
        "Is Gateway:",
        "Is internal:",
    ]

    def __init__(self, neutronRouterPointer):
        self.neutronRouterPointer = None
        self.topLevelGUI = None
        self.buttonCreateInt = None
        self.buttonDeleteInt = None
        self.radioBtnsList = []
        self.interfaces = []
        self.labelsList = []
        self.entryList = []
        self.radBtnChoice = None

        if neutronRouterPointer is None:
            raise AssertionError("Assertion Triggered: Neutron Router does not exist")

        self.neutronRouterPointer = neutronRouterPointer

    def onButtonConfigureNetwork(self, event):
        return

    def displayDialog(self):
        topLevel = Toplevel()
        topLevel.title("Created Interface")
        topLevel.iconbitmap('ibm.ico')

        labelTitle = Label(topLevel, text="Created Interface (New Network/Subnet and Port)")
        labelTitle.pack()
        labelNetName = Label(topLevel,  text=self.neutronRouterPointer.network.net.name)
        labelNetName.pack()
        labelNetID   = Label(topLevel,  text=self.neutronRouterPointer.network.net.id)
        labelNetID.pack()
        labelPortName = Label(topLevel, text=self.neutronRouterPointer.port.name)
        labelPortName.pack()
        labelPortId   = Label(topLevel, text=self.neutronRouterPointer.port.id)
        labelPortId.pack()


    def onButtonCreateInt(self, event):

        isInternal = True
        if self.radBtnChoice.get() == 2:
            isInternal = False

        self.neutronRouterPointer.createRouterInterface(self.entryList[0].get(),
                                                        self.entryList[1].get(),
                                                        self.entryList[2].get(),
                                                        self.entryList[3].get(),
                                                        "",
                                                        self.entryList[4].get(),
                                                        self.entryList[5].get(),
                                                        isInternal)

        self.displayDialog()

        return

    def createGUI(self):
        self.topLevelGUI  = Toplevel()
        self.topLevelGUI.geometry("700x160")
        self.topLevelGUI.title("Router Interface Config")
        self.topLevelGUI.iconbitmap('ibm.ico')
        self.topLevelGUI.resizable(0, 0)

        self.radBtnChoice = IntVar()
        self.radBtnChoice.set(1)

        xPixelPitch   = 5
        yStepInterval = 0
        for i in range(0, 8, 1):
            self.labelsList.append(Label(self.topLevelGUI, text=self.labelText[i]))

            if ((i % 3) == 0) and (i != 0) and (i < 7):
                xPixelPitch += 265
            yStepInterval = i % 3

            self.labelsList[i].place(x=xPixelPitch, y=(yStepInterval*40)+5)
            if i < 6:
                self.entryList.append((Entry(self.topLevelGUI)))
                self.entryList[i].place(x=xPixelPitch+125, y=(yStepInterval*40)+5)
            else:
                self.radioBtnsList.append(Radiobutton(self.topLevelGUI, value=i-6, variable=self.radBtnChoice))
                self.radioBtnsList[i-6].place(x=xPixelPitch+125, y=(yStepInterval*40)+5)

        buttonCreateInt = Button(self.topLevelGUI, text='Create Interface')
        buttonCreateInt.place(x=5, y=120)

        buttonCreateInt.bind('<Button-1>', self.onButtonCreateInt)

