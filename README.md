# jeopardy_score
This is a Python program that uses PySimpleGUI to keep track of the score in a game of Jeopardy. After the inital setup there is a host window for adding and subtracting the score and a client window which has a table with the player names, scores, and scores from the round before. This program also has support for getting the question number from PowerPoint. Instructions on how to do this will be available soon.
## Installation
Simply clone this repository and run main.py. You may need to add PySimpleGUI (You can do this by running `pip install pysimplegui` in cmd or terminal). Note that this program has only been tested on Windows 10, so your mileage may vary on other operating systems. If you find any bugs, please let me know!

### Powerpoint Setup (Optional)
There are two ways to setup a PowerPoint presentation with this program: Use the included sample presentation or create a new presentation manually. Note that the included presentation contains a macro for updating the text document for the scorer to read, so keep that in mind.

#### Using the Included PowerPoint Presentation
1. Open the `Jeopardy Macro Template.pptm` included in this repository and accept all dialogs warning you about macros (this is required, but proceed at your own risk).
2. Add the Developer tab to the Ribbon using these instructions: https://www.howtogeek.com/400301/how-to-add-the-developer-tab-to-the-ribbon/ (they are for Word but should still work).
3. In the Developer tab click on the `Macros` button and the macro in the popup called "GetSlideNumber." Click "Edit."
4. In the new window that appears, locate the third line of the inner window.
5. Replace "C:\MyFileDirectory" in "C:\MyFileDirectory\SlideNotes.txt" with the directory that contains the Python scorer program. If you want to use a different directory/filename you will need to edit the Python scorer script.
6. When you are done, click File>Save, then close the window.
7. You will notice on the question slides in the presentation a transparent rectangle that covers the entire slide, do not delete these!
8. If you want to make a question a Daily Double, change the slide notes to "DD".

#####
1. Create a new presentation in PowerPoint and save it as a PowerPoint Macro-Enabled Presentation (.pptm).
2. Add the developer tab to the ribbon if you don't already have it using these instructions: https://www.howtogeek.com/400301/how-to-add-the-developer-tab-to-the-ribbon/ (they are for Word but should still work).
3. In the Developer tab click on the `Macros` button and type a name for the macro (eg. "GetSlideNumber"). Click Create.
4. In the inner window of the new window paste in the code below between `Sub *yourMacroName*()` and `End Sub`
    ```
    Dim sFileName As String
    sFileName = "C:\MyFileDirectory"

    Open sFileName For Output As #1
    Print #1, Replace(SlideShowWindows(1).View.Slide.NotesPage.Shapes.Placeholders(2).TextFrame.TextRange.Text, Chr(13), vbCrLf)
    Close #1
    ```
5. When you are done, click File>Save, then close the window.
6. Go to a slide in your presentation with a Jeopardy question and insert a shape. Then in the search bar, search for "Action Settings."
7. In the new popup, select "Run macro" and the name of your macro. Click "OK."
8. Finally, on the slide with the shape you made, add the column letter and row number on the Jeopardy board (eg. A2 is the first Jeopardy column on the second row). To map the question to a Daily Double,, set the text to "DD". The mappings can be changed in the `board.json` file in the repository.

##### Presenting with PowerPoint and Jeopardy Scorer
Start the presentation in PowerPoint and run `main.py` from the repository. Once you have entered the players, you will see two fields related to the PowerPoint presentation: "Current Question" and "Question Value." When you get to a question slide in your presentation click near one of the corners of the slide (or wherever you put your shape if you made the presentation manually) and you will see the fields in the scorer update. The add and subtract buttons in the scorer will add or subtract the amount in question value. You can change the question values in the `board.json` if you want.
