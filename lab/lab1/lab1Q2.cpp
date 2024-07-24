#include <algorithm>
#include <utility>
#include <iostream>
using namespace std;

pair<long, long> minmaxFromArray(long _array[], short _array_length, short first_index, short last_index) {
        if (first_index == last_index) {
            return make_pair(_array[first_index], _array[first_index]); 
        }
        
        pair<long ,long> final_result = minmaxFromArray(_array,_array_length,first_index + 1,last_index);
        
        return make_pair(min(_array[first_index], final_result.first), max(_array[first_index], final_result.second)); 
        
}
   