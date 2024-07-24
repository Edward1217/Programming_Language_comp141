#include <iostream>
#include <vector>
#include <algorithm>
#include <utility>
using namespace std;

vector<pair<string, string> > setDictionaryEntry(vector<pair<string, string> > dictionary,string _key, string _value, int first_index) {
        if (first_index == dictionary.size()-1) {
            vector<pair<string, string> > dictionary1 = dictionary;
            dictionary1.push_back(pair<string, string>(_key, _value));
            return dictionary1;
        }

        
        
        if (dictionary[first_index].first == _key) {
            vector<pair<string, string> > dictionary1 = dictionary;
            dictionary1[first_index].second = _value;
            return dictionary1;
        }
        
        return setDictionaryEntry(dictionary, _key,_value, first_index + 1);
}