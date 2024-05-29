class StyleSheets:
  APP: str = """
    * {
      font-size: 14pt;
    }
    #heading {
      font-size: 18pt;
      font-weight: bold;
    }
    QLineEdit, QPushButton, QLabel {
      padding: 0.25em;
    }
    QPushButton {
      padding: 0.25em 1em;
    }
    #goalselectorscrollview {
      padding: 0.25em;
    }
    #goalselectorscrollview QPushButton {
      background-color: transparent;
      font-size: 12pt;
      padding: 0.1em;
      border: none;
    }
    #goalselectorscrollview QPushButton:checked {
      background-color: #649bff;
      border: none;
    }
    #goalselectorscrollview QLabel {
      background-color: transparent;
      font-size: 12pt;
      padding: 0em;
    }
    """