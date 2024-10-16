#include <iostream>

using namespace std;

#define problems 5
#define exit -1



int main(){
    while(true){
        // cout << "Enter Problem number (from 1 to " << problems << ")\n";
        // int Qn;
        // cin >> Qn;
        int a,b;
        cin >> a >> b;
        for(int i = 0;i < 5;i++){
            cout << a+b << endl;
        }
    }
    return 0;
}
