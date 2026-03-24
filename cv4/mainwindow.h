#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QGridLayout>


class MainWindow : public QWidget
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
public slots:
    void digitClicked();
    void operatorClicked();
    void equalsClicked();
    void clearClicked();
    void dotClicked();
    void toggleSignClicked();

private:
    QLineEdit *display;
    QPushButton *digitButtons[10];
    double firstNum = 0;
    QString pendingOperator;
    bool waitingForSecondNum = false;
};
#endif // MAINWINDOW_H
