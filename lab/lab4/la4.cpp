#include <iostream>
#include <regex>
#include <string>
#include <sstream> 
using namespace std;

int main() {
    string token;
    double number_token;
    cout << "Please enter a single token here: ";
    cin >> token;
    
    stringstream ss(token);
    regex interger_regex("^[0-9]+$");
    regex punctuation_regex("^[+*(),]$");

    if (regex_match(token,interger_regex)) {
        if (ss >> number_token) {
            cout << number_token <<endl;
            cout << "number" << endl;
        }
    }
    else if (regex_match(token, punctuation_regex)) {
        cout << token << "punc" <<endl;

    }
    else {
        cout << "undefined yet" << endl;
    }
    return 0;
}


