"""
COPYRIGHT HỒ QUỐC THÁI 10A4 2021-2022
DO NOT USE WITHOUT PERMISSION
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import rgba

# constant Value
# Sizes
SIZE_HINT_X = .25
SIZE_HINT_Y = 1 / 7

POS_HINT_X = SIZE_HINT_X
POS_HINT_Y = SIZE_HINT_Y
# Colors
FULL_BLACK = (0, 0, 0, 1)
DIGIT_COLOR = (0, 0, 0, .9)
EQUAL_COLOR = (245 / 255, 143 / 255, 0, 1)
OTHER_COLORS = (0, 0, 0, .6)
# Font Sizes
DIGIT_SIZE = "31dp"
OPERATOR_SIZE = "29dp"
LARGE_FONT_SIZE = "100dp"
SMALL_FONT_SIZE = "25dp"
OTHER_FONT_SIZE = "30dp"

listO = ['*', '+', '-', '/']

Window.clearcolor = rgba(54, 53, 53, 1)

class Calculator:
    def __init__(self):
        # create a layout for button
        self.layout = FloatLayout(size=Window.size)

        # all the digits on the calculator

        self.digits = {
            7: (0, POS_HINT_Y * 3), 8: (POS_HINT_X, POS_HINT_Y * 3), 9: (POS_HINT_X * 2, POS_HINT_Y * 3),  # 7 8 9
            4: (0, POS_HINT_Y * 2), 5: (POS_HINT_X, POS_HINT_Y * 2), 6: (POS_HINT_X * 2, POS_HINT_Y * 2),  # 4 5 6
            1: (0, POS_HINT_Y), 2: (POS_HINT_X, POS_HINT_Y), 3: (POS_HINT_X * 2, POS_HINT_Y),  # 1 2 3
            0: (POS_HINT_X, 0), '.': (POS_HINT_X * 2, 0),  # 0 .
        }
        # operations
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.currentExpression = ''
        self.totalExpression = ''

        # creating expressions display
        self.currentExpressionText, self.totalExpressionText = self.addTextInputExpression()

        # displaying expression, buttons
        self.addAllButtons()
        self.layout.add_widget(self.currentExpressionText)
        self.layout.add_widget(self.totalExpressionText)

    # region Buttons
    def addAllButtons(self):
        self.createDigitButtons()
        self.createOperatorButton()
        self.createSpecialButton()

    # create the digit button using the dict
    def createDigitButtons(self):
        for digit, posHint in self.digits.items():
            button = Button(text=str(digit),
                            size_hint=(SIZE_HINT_X, SIZE_HINT_Y),
                            pos_hint={'x': posHint[0], 'y': posHint[1]},
                            bold=True,
                            background_normal='',
                            background_color=DIGIT_COLOR,
                            on_press=lambda x=digit: self.addToExpression(x.text)
                            )
            button.font_size = DIGIT_SIZE

            self.layout.add_widget(button)

    # create operator +=*/
    def createOperatorButton(self):

        indexDivider = 4
        for _, symbol in self.operations.items():
            button = Button(text=str(symbol),
                            size_hint=(SIZE_HINT_X, SIZE_HINT_Y),
                            pos_hint={'x': POS_HINT_X * 3, 'y': POS_HINT_Y * indexDivider},
                            background_normal='',
                            background_color=OTHER_COLORS,
                            on_press=lambda x=symbol: self.appendOperator(x.text),
                            )
            button.font_size = OPERATOR_SIZE

            self.layout.add_widget(button)
            indexDivider -= 1

    def createSpecialButton(self):
        # create Equal Button
        equalButton = Button(text='=',
                             size_hint=(SIZE_HINT_X, SIZE_HINT_Y),
                             pos_hint={'x': POS_HINT_X * 3, 'y': 0},
                             background_normal='',
                             background_down='',
                             background_color=EQUAL_COLOR,
                             on_press=lambda x: self.evaluate(),
                             bold=True
                             )
        equalButton.font_size = OTHER_FONT_SIZE

        # create clear Button
        clearButton = Button(text='C',
                             size_hint=(SIZE_HINT_X, SIZE_HINT_Y),
                             pos_hint={'x': POS_HINT_X * 2, 'y': POS_HINT_Y * 4},
                             background_normal='',
                             background_color=OTHER_COLORS,
                             on_press=lambda x: self.clearButton()
                             )
        clearButton.font_size = OTHER_FONT_SIZE

        square = Button(text='x\u00b2',
                        size_hint=(SIZE_HINT_X, SIZE_HINT_Y),
                        pos_hint={'x': 0, 'y': POS_HINT_Y * 4},
                        background_normal='',
                        background_color=OTHER_COLORS,
                        on_press=lambda x: self.squareCalc(),
                        )
        square.font_size = OTHER_FONT_SIZE

        squareRoot = Button(text='\u221a',
                            size_hint=(SIZE_HINT_X, SIZE_HINT_Y),
                            pos_hint={'x': POS_HINT_X, 'y': POS_HINT_Y * 4},
                            background_normal='',
                            background_color=OTHER_COLORS,
                            on_press=lambda x: self.squareRootCalc(),
                            )
        squareRoot.font_size = OTHER_FONT_SIZE

        switchNum = Button(text='+/-',
                           size_hint=(SIZE_HINT_X, SIZE_HINT_Y),
                           pos_hint={'x': 0, 'y': 0},
                           background_normal='',
                           background_color=DIGIT_COLOR,
                           on_press=lambda x: self.switchNumCalc(),
                           )
        switchNum.font_size = OTHER_FONT_SIZE

        self.layout.add_widget(clearButton)
        self.layout.add_widget(equalButton)
        self.layout.add_widget(square)
        self.layout.add_widget(squareRoot)
        self.layout.add_widget(switchNum)

    # endregion
    # region InputExpression
    def addTextInputExpression(self):
        currentExpression1 = TextInput(
            text=self.totalExpression,
            halign='right',
            size_hint=(1, .2),
            pos_hint={'x': 0, 'y': POS_HINT_Y * 5},
            multiline=False,
            readonly=True,
            background_color=OTHER_COLORS,
            background_normal='',
            foreground_color=(1, 1, 1, 1),
            cursor_blink=False,
            text_validate_unfocus=True,
        )
        currentExpression1.font_size = LARGE_FONT_SIZE
        currentExpression1.padding_y = [currentExpression1.height / 2, 0]

        totalExpression1 = TextInput(
            text=self.currentExpression,
            halign='right',
            size_hint=(1, .089),
            pos_hint={'x': 0, 'y': POS_HINT_Y * 5 + .2},
            multiline=False,
            readonly=True,
            background_color=OTHER_COLORS,
            background_normal='',
            foreground_color=(1, 1, 1, 1),
            cursor_blink=False,
            text_validate_unfocus=True,
        )
        totalExpression1.font_size = SMALL_FONT_SIZE
        totalExpression1.padding_y = (totalExpression1.height / 1.5, 0)
        totalExpression1.padding_x = (0, totalExpression1.width / 5)

        return currentExpression1, totalExpression1

    # endregion
    # region functionality

    # updating the current expression
    def updateLabel(self):
        self.currentExpressionText.text = self.currentExpression[:11]

    # updating total expression
    def updateTotalLabel(self):
        self.totalExpressionText.text = self.totalExpression

    # add the digits to expression
    def addToExpression(self, value):
        # check if the value is an Error
        if self.currentExpression == 'Error':
            self.clearButton()

        self.currentExpression += str(value)
        self.updateLabel()

    # add operators to expression
    def appendOperator(self, operator):
        # check if the value is an Error
        if self.currentExpression == 'Error':
            self.clearButton()
            return

        if operator == '\u00D7':
            operator = '*'
        elif operator == '\u00F7':
            operator = '/'

        self.currentExpression += operator
        # check if is there anything on the current operator
        if self.totalExpression == '' and self.currentExpression in listO:
            self.currentExpression = ''
            return

        self.totalExpression += self.currentExpression
        self.currentExpression = ''

        # check if there's already an expression
        # create a list of current totalExpression and operator to check
        listS = [word for word in self.totalExpression]

        # check if the last pos and the second last pos is an operator

        if listS[-1] in listO and listS[-2] in listO:
            # del the last pos
            listS.pop(-1)
            # join the list to a new string
            newValue = ''.join(listS)
            # set total expression to new value
            self.totalExpression = str(newValue)

        self.updateLabel()
        self.updateTotalLabel()

    def clearButton(self):
        # clear all the expression
        self.currentExpression = ''
        self.totalExpression = ''

        self.updateLabel()
        self.updateTotalLabel()

    def squareCalc(self):
        if self.currentExpression == 'Error':
            self.clearButton()
            self.currentExpression = '0'

        if self.currentExpression not in listO and self.currentExpression != '':
            self.currentExpression = str(eval(f'{self.currentExpression}**2'))
            self.updateLabel()

    def squareRootCalc(self):
        if self.currentExpression == 'Error':
            self.clearButton()
            self.currentExpression = '0'

        if self.currentExpression not in listO and self.currentExpression != '':
            self.currentExpression = str(eval(f'{self.currentExpression}**0.5'))
            self.updateLabel()

    def switchNumCalc(self):
        if self.currentExpression == 'Error':
            self.clearButton()
            self.currentExpression = '0'
        if self.currentExpression not in listO and self.currentExpression != '':
            self.currentExpression = str(eval(f'{self.currentExpression}*-1'))
            self.updateLabel()

    # calculate the expression
    def evaluate(self):
        # if this current expression is Error, append it as 0
        if self.currentExpression == 'Error':
            self.clearButton()
            self.currentExpression = '0'

        self.totalExpression += self.currentExpression
        self.updateTotalLabel()

        # try calculating the expression
        try:
            answer = str(eval(self.totalExpression))
        except ZeroDivisionError:  # bad error
            answer = "Error"
        except:
            answer = 'Error'

        self.currentExpression = answer

        self.totalExpression = ""
        self.updateLabel()

    # endregion

    # return the layout
    def getLayout(self):
        return self.layout


# build the app: Name-App
class CalculatorApp(App):
    def build(self):
        calc = Calculator()
        return calc.getLayout()


# run the app
if __name__ == "__main__":
    CalculatorApp().run()
