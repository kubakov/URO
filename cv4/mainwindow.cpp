#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QWidget(parent)
{
    setWindowTitle("Calculator");
    setFixedSize(280,420);

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(10, 10, 10, 10);
    mainLayout->setSpacing(6);

    display = new QLineEdit("0");
    display->setAlignment(Qt::AlignRight);
    display->setReadOnly(true);
    display->setFixedHeight(60);
    mainLayout->addWidget(display);

    for(int i = 0; i < 10; i++){
        digitButtons[i] = new QPushButton(QString::number(i));
        digitButtons[i]->setFixedHeight(55);
        connect(digitButtons[i], SIGNAL(clicked()), this, SLOT(digitClicked()));
    }

    QPushButton *btnClear = new QPushButton("AC");
    QPushButton *btnToggleSign = new QPushButton("+/-");
    QPushButton *btnModulo = new QPushButton("%");
    QPushButton *btnDiv = new QPushButton("/");
    QPushButton *btnMul = new QPushButton("*");
    QPushButton *btnSub = new QPushButton("-");
    QPushButton *btnAdd = new QPushButton("+");
    QPushButton *btnEquals = new QPushButton("=");
    QPushButton *btnDot = new QPushButton(".");

    QPushButton *opButtons[] = {btnClear, btnToggleSign, btnModulo, btnDiv, btnMul,
                                btnSub, btnAdd, btnEquals, btnDot};

    for(QPushButton *btn : opButtons){
        btn->setFixedHeight(55);
    }

    connect(btnClear, SIGNAL(clicked()), this, SLOT(clearClicked()));
    connect(btnToggleSign, SIGNAL(clicked()), this, SLOT(toggleSignClicked()));
    connect(btnModulo, SIGNAL(clicked()), this, SLOT(operatorClicked()));
    connect(btnDiv, SIGNAL(clicked()), this, SLOT(operatorClicked()));
    connect(btnMul, SIGNAL(clicked()), this, SLOT(operatorClicked()));
    connect(btnSub, SIGNAL(clicked()), this, SLOT(operatorClicked()));
    connect(btnAdd, SIGNAL(clicked()), this, SLOT(operatorClicked()));
    connect(btnEquals, SIGNAL(clicked()), this, SLOT(equalsClicked()));
    connect(btnDot, SIGNAL(clicked()), this, SLOT(dotClicked()));

    QGridLayout *grid = new QGridLayout;
    grid->setSpacing(6);

    grid->addWidget(btnClear, 0, 0);
    grid->addWidget(btnToggleSign, 0, 1);
    grid->addWidget(btnModulo, 0, 2);
    grid->addWidget(btnDiv, 0, 3);

    grid->addWidget(digitButtons[7], 1, 0);
    grid->addWidget(digitButtons[8], 1, 1);
    grid->addWidget(digitButtons[9], 1, 2);
    grid->addWidget(btnMul, 1, 3);

    grid->addWidget(digitButtons[4], 2, 0);
    grid->addWidget(digitButtons[5], 2, 1);
    grid->addWidget(digitButtons[6], 2, 2);
    grid->addWidget(btnSub, 2, 3);

    grid->addWidget(digitButtons[1], 3, 0);
    grid->addWidget(digitButtons[2], 3, 1);
    grid->addWidget(digitButtons[3], 3, 2);
    grid->addWidget(btnAdd, 3, 3);

    grid->addWidget(digitButtons[0], 4, 0, 1, 2);
    grid->addWidget(btnDot, 4, 2);
    grid->addWidget(btnEquals, 4, 3);

    mainLayout->addLayout(grid);
}

MainWindow::~MainWindow() {}

void MainWindow::digitClicked()
{
    QPushButton *btn = qobject_cast<QPushButton*>(sender());
    QString digit = btn->text();

    if (waitingForSecondNum) {
        display->setText(QString::number(firstNum) + pendingOperator + digit);
        waitingForSecondNum = false;
    } else {
        display->setText(display->text() == "0" ? digit : display->text() + digit);
    }
}

void MainWindow::toggleSignClicked()
{
    double value = display->text().toDouble();
    if(value != 0){
        display->setText(QString::number(value * -1, 'g', 10));
    }
}

void MainWindow::dotClicked()
{
    if (waitingForSecondNum) {
        display->setText("0.");
        waitingForSecondNum = false;
        return;
    }
    if (!display->text().contains('.'))
        display->setText(display->text() + ".");
}

void MainWindow::operatorClicked()
{
    QPushButton *btn = qobject_cast<QPushButton*>(sender());

    QString text = display->text();
    if(!pendingOperator.isEmpty() && text.endsWith(pendingOperator)){
        text.chop(1);
    }
    firstNum = text.toDouble();
    pendingOperator = btn->text();
    waitingForSecondNum = true;
    display->setText(QString::number(firstNum) + pendingOperator);
}

void MainWindow::equalsClicked()
{
    if (pendingOperator.isEmpty()) return;

    QString text = display->text();
    int opIndex = text.lastIndexOf(pendingOperator);
    double second = text.mid(opIndex + 1).toDouble();
    double result = 0;

    if      (pendingOperator == "+") result = firstNum + second;
    else if (pendingOperator == "-") result = firstNum - second;
    else if (pendingOperator == "*") result = firstNum * second;
    else if (pendingOperator == "%") result = fmod(firstNum, second);
    else if (pendingOperator == "/") {
        if (second == 0) { display->setText("Can't divide by 0"); return; }
        result = firstNum / second;
    }

    display->setText(QString::number(result, 'g', 10));
    pendingOperator.clear();
    waitingForSecondNum = false;
}

void MainWindow::clearClicked()
{
    display->setText("0");
    firstNum = 0;
    pendingOperator.clear();
    waitingForSecondNum = false;
}