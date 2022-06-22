# Repository with a program to rectify and extract features from the images of the clerk's terminal

Allows image processing using image pre-processing techniques (mathematical morphology, edge detection, etc), using the result as input to easyOCR to extract characters from the clerk's terminal screen.

Image output: Generating a .txt file with the characters extracted

Note: Recommended to use Conda virtual environment to run application.

The required list of libraries to run the application is:

- pip install opencv-python==4.5.4.60
- conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
- pip install easyocr
- pip install tesseract
- pip install pytesseract
- pip install gdown

Note: There is a version of the project in jupyter notebook with comments in Portuguese on this link: 
https://colab.research.google.com/drive/1hrJATWcw9boarnxjtmzhAuEKjytNH6cu?usp=sharing
