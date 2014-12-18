import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

#
# LineIntensityProfile
#

class LineIntensityProfile(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Line Intensity Profile" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Longquan Chen (Fraunhofer MeVis)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# LineIntensityProfileWidget
#

class LineIntensityProfileWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # First volume selector
    #
    self.inputSelector1 = slicer.qMRMLNodeComboBox()
    self.inputSelector1.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector1.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector1.selectNodeUponCreation = True
    self.inputSelector1.addEnabled = False
    self.inputSelector1.removeEnabled = False
    self.inputSelector1.noneEnabled = False
    self.inputSelector1.showHidden = False
    self.inputSelector1.showChildNodeTypes = False
    self.inputSelector1.setMRMLScene( slicer.mrmlScene )
    self.inputSelector1.setToolTip( "Pick the first input to the algorithm." )
    parametersFormLayout.addRow("First Volume: ", self.inputSelector1)
    
    #
    # Second volume selector
    #
    self.inputSelector2 = slicer.qMRMLNodeComboBox()
    self.inputSelector2.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector2.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector2.selectNodeUponCreation = True
    self.inputSelector2.addEnabled = False
    self.inputSelector2.removeEnabled = False
    self.inputSelector2.noneEnabled = False
    self.inputSelector2.showHidden = False
    self.inputSelector2.showChildNodeTypes = False
    self.inputSelector2.setMRMLScene( slicer.mrmlScene )
    self.inputSelector2.setToolTip( "Pick the second input to the algorithm." )
    parametersFormLayout.addRow("Second Volume: ", self.inputSelector2)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.outputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.outputSelector.selectNodeUponCreation = False
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = False
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # Ruler selector
    #
    self.rulerSelector = slicer.qMRMLNodeComboBox ()
    self.rulerSelector.nodeTypes = ( ("vtkMRMLAnnotationRulerNode"), "" )
    self.rulerSelector.selectNodeUponCreation = True
    self.rulerSelector.addEnabled = False
    self.rulerSelector.removeEnabled = False
    self.rulerSelector.noneEnabled = False
    self.rulerSelector.showHidden = False
    self.rulerSelector.showChildNodeTypes = False
    self.rulerSelector.setMRMLScene( slicer.mrmlScene )
    self.rulerSelector.setToolTip( "Pick the ruler to sample along." )
    parametersFormLayout.addRow("Ruler: ", self.rulerSelector)

    #
    #Number of sample points parameter
    #

    self.numOfPointsField = qt.QSpinBox()
    self.numOfPointsField.setRange(1, 2000)
    self.numOfPointsField.value = 100
    self.numOfPointsField.setSingleStep(1)
    parametersFormLayout.addRow("Num Of Points: ", self.numOfPointsField)
    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = True
    parametersFormLayout.addRow(self.applyButton)


    self.chartNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector1.currentNode() and self.inputSelector2.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = LineIntensityProfileLogic()
    print("Run the algorithm")
    self.changeRulerColor()
    logic.run(self.inputSelector1.currentNode(), self.inputSelector2.currentNode(), self.rulerSelector.currentNode(), self.numOfPointsField, self.chartNode)


  def changeRulerColor(self):
    #-------------------------
    #Adjust the ruler color according to current selected image in the viewer

    #Get the first viewer and get the background image volume inside
    SliceComRed = slicer.util.getNode("SliceComposite")
    Volume_b = slicer.mrmlScene.GetNodeByID(SliceComRed.GetBackgroundVolumeID())
    #Check the current
    VolumeName = self.inputSelector1.currentNode().GetName()
    Volume_a1 = slicer.util.getNode(VolumeName)

    VolumeName = self.inputSelector2.currentNode().GetName()
    Volume_a2 = slicer.util.getNode(VolumeName)

    #for Ruler in self.rulerSelector.nodes:
    listNodeID = "vtkMRMLAnnotationHierarchyNode2"
    annotationHierarchyNode = slicer.mrmlScene.GetNodeByID(listNodeID)
    totalRuleNum = annotationHierarchyNode.GetNumberOfChildrenNodes()
    currentName = self.rulerSelector.currentNode().GetName()
    currentIndex = 0
    for i in range(totalRuleNum):
      self.rulerSelector.setCurrentNodeIndex(i)
      currentNameTemp = self.rulerSelector.currentNode().GetName()
      if self.rulerSelector.currentNode().GetName() == currentName:
        currentIndex = i
      Ruler = slicer.util.getNode(currentNameTemp)
      RulerDisplayNodeID = Ruler.GetDisplayNodeID()
      Line = slicer.util.getNode(RulerDisplayNodeID)
      red = [1,0,0]
      green = [0,1,0]
      if (Volume_a1 == Volume_b) and (not (Volume_a1 == Volume_a2)): # check if the first input selector is the same as the showed image volume
        Line.SetColor(red) # the color red, corresponding to #FF0000
      elif Volume_a2 == Volume_b:
        Line.SetColor(green) # the color green, corresponding to #FF0000
      elif (not (Volume_a1 == Volume_b)) and (not (Volume_a2 == Volume_b)): # when the display volume is not the same as any of the input volume
        Line.SetColor(green) # the color green, corresponding to #FF0000
    self.rulerSelector.setCurrentNodeIndex(currentIndex)
    #-------------------------

#
# LineIntensityProfileLogic
#

class LineIntensityProfileLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  def __init__(self):
    self.imageSamples = None

  def getImageSamples(self):
    return self.imageSamples

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    self.delayDisplay(description)

    if self.enableScreenshots == 0:
      return

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, self.screenshotScaleFactor, imageData)

  def run(self,volumeNode1,volumeNode2, rulerNode, numOfPointsField, chartNode):
    """
    Run the actual algorithm
    """

    print("LineIntensityProfileLogic run() called")
    if not rulerNode or (not volumeNode1 and not volumeNode2):
      print('Inputs are not initialized!')
      return

    volumeSamples1 = None
    volumeSamples2 = None
    numOfPoints = numOfPointsField.value
    if volumeNode1:
      [volumeSamples1, distanceArray1] = self.probeVolume(volumeNode1, rulerNode, numOfPoints)
    if volumeNode2:
      [volumeSamples2, distanceArray2] = self.probeVolume(volumeNode2, rulerNode, numOfPoints)

    imageSamples = [volumeSamples1, volumeSamples2]
    distanceArrays = [distanceArray1, distanceArray2]
    legendNames = [volumeNode1.GetName()+' - '+rulerNode.GetName(), volumeNode2.GetName()+' - '+rulerNode.GetName()]
    self.imageSamples = imageSamples # for testing purpose
    self.showChart(imageSamples, legendNames, distanceArrays, chartNode)
    return True

  def showChart(self, samples, names, distanceArrays, chartNode):
    print("Logic showing chart")

    # Switch to a layut containing a chart viewer
    lm = slicer.app.layoutManager()
    lm.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpQuantitativeView)

    # initialize double array MRML node for each sample list,
    #  since this is what chart view MRML node needs
    doubleArrays = []
    for sample in zip(distanceArrays, samples):
      arrayNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLDoubleArrayNode())
      array = arrayNode.GetArray()
      nDataPoints = len(sample[0])
      array.SetNumberOfTuples(nDataPoints)
      array.SetNumberOfComponents(3)
      for i in range(nDataPoints):
        array.SetComponent(i, 0, sample[0][i])
        array.SetComponent(i, 1, sample[1].GetTuple1(i))
        array.SetComponent(i, 2, 0)

      doubleArrays.append(arrayNode)

    # get the chart view MRML node
    cvNodes = slicer.mrmlScene.GetNodesByClass('vtkMRMLChartViewNode')
    cvNodes.SetReferenceCount(cvNodes.GetReferenceCount()-1)
    cvNodes.InitTraversal()
    cvNode = cvNodes.GetNextItemAsObject()

    # ChartNode is passed from the widget
    chartNode.ClearArrays()
    colorScheme = ["#FF0000","#7CFC00"] # "#FF0000" is red,  "#7CFC00" is green, by default is green
    for pairs in zip(names, doubleArrays, colorScheme):
      chartNode.AddArray(pairs[0], pairs[1].GetID())
      chartNode.SetProperty(pairs[0], "color", pairs[2])
    cvNode.SetChartNodeID(chartNode.GetID())
    return


  def probeVolume(self, volumeNode, rulerNode, numOfPoints):
    
    #get ruler end points in RAS coordinates system
    p0ras = rulerNode.GetPolyData().GetPoint(0) + (1,)
    p1ras = rulerNode.GetPolyData().GetPoint(1) + (1,)
    import math, numpy
    lineLength = math.sqrt((p0ras[0]-p1ras[0])*(p0ras[0]-p1ras[0]) + (p0ras[1]-p1ras[1])*(p0ras[1]-p1ras[1]) + (p0ras[2]-p1ras[2])*(p0ras[2]-p1ras[2]))
    distanceArray = [0]
    if (numOfPoints > 1):
      distanceArray = numpy.linspace(0,lineLength,numOfPoints)


    #The transformation matrix from RAS to IJK coordinates systems
    ras2ijk = vtk.vtkMatrix4x4()
    volumeNode.GetRASToIJKMatrix(ras2ijk)
    p0ijk = [int(round(c)) for c in ras2ijk.MultiplyPoint(p0ras)[:3]]
    p1ijk = [int(round(c)) for c in ras2ijk.MultiplyPoint(p1ras)[:3]]

    #Create the VTK sampling line
    line = vtk.vtkLineSource()
    line.SetResolution(numOfPoints)
    line.SetPoint1(p0ijk[0], p0ijk[1], p0ijk[2])
    line.SetPoint2(p1ijk[0], p1ijk[1], p1ijk[2])

    #Creat the VTK probe filter
    probe = vtk.vtkProbeFilter()
    probe.SetInputConnection(line.GetOutputPort())
    probe.SetSourceData(volumeNode.GetImageData())
    probe.Update()

    # return the sampled array
    return probe.GetOutput().GetPointData().GetArray('ImageScalars'), distanceArray


class LineIntensityProfileTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_LineIntensityProfile1()

  def test_LineIntensityProfile1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = LineIntensityProfileLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    # initialize ruler node in a known location
    rulerNode = slicer.vtkMRMLAnnotationRulerNode()
    slicer.mrmlScene.AddNode(rulerNode)
    rulerNode.SetPosition1(-65,110,60)
    rulerNode.SetPosition2(-15,60,60)
    rulerNode.SetName('Test')
    numOfPointsField = qt.QSpinBox()
    numOfPointsField.value = 100
    chartNode = slicer.mrmlScene.AddNode(slicer.vtkMRMLChartNode())

    # initialize input selectors
    moduleWidget = slicer.modules.LineIntensityProfileWidget
    moduleWidget.rulerSelector.setCurrentNode(rulerNode)
    moduleWidget.inputSelector1.setCurrentNode(volumeNode)
    moduleWidget.inputSelector2.setCurrentNode(volumeNode)


    self.delayDisplay('Inputs initialized!')

    # run the logic with the initialized inputs
    moduleWidget.onApplyButton()
    self.delayDisplay('If you see a ruler and a plot - test passed!')

    # here we check the sample is correct or not
    GroundTruth = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0 \
                   ,0.0499952547252 ,0.132161304355,0.157250195742,0.182541355491 ,0.224097684026,0.307691186666,0.421751081944,0.539702475071,0.566307783127,0.502181112766,0.466381758451 \
                   ,0.454870164394 ,0.451874107122 ,0.45154094696,0.445982009172,0.434947699308,0.422306239605,0.413488268852,0.409934103489,0.414202958345,0.409307956696 \
                   ,0.397122174501,0.397800117731,0.411369532347,0.429417848587,0.439514577389,0.423818171024,0.40110757947,0.386767745018,0.379366248846,0.370953738689,0.36441424489 \
                   ,0.36140397191,0.367857933044,0.38929861784,0.418379157782,0.408268928528,0.379027366638,0.332919150591,0.297374159098,0.296240001917,0.311986237764,0.350458532572 \
                   ,0.370930314064,0.357974469662,0.326200008392,0.316009640694,0.312490910292,0.32052642107,0.316521972418,0.279196560383,0.244257837534,0.238702788949,0.255041092634 \
                   ,0.280225723982,0.320494830608,0.28876376152,0.277780592442,0.253679126501,0.247220918536,0.244660764933]

    logic.run(volumeNode, volumeNode, rulerNode, numOfPointsField, chartNode)
    sample = logic.getImageSamples()[0]
    isTestValid = True
    for i in range(numOfPointsField.value):
      if abs(sample.GetTuple1(i)-float(GroundTruth[i])) > 0.000001:
        isTestValid = False

    if isTestValid:
      self.delayDisplay('Sample point test passed!')
    else:
      self.delayDisplay('Sample point test failed!')
    # here we check the sample is correct or not
