/*
 * Find the longest arithematic progression in an array using DP Method
 * Reference:- geeksforgeeks
 * Author: Rohith
 */
 
#include <iostream>
#include <vector>
#include <algorithm>
 
using namespace std;
 
void llap(vector<int> v){
	int n = v.size();
	vector<vector<int> > dp(n, vector<int>(n,0));
	int max_len=2, ap_term, ap_start;
	for(int i=0; i<n; i++) dp[i][n-1] = 2;
	for(int j=n-2; j>=1; j--){
		int i=j-1,k=j+1;
		while(i>=0 && k <= n-1){
			if(v[i] + v[k] < (2*v[j])) k++;
			else if(v[i] + v[k] > (2*v[j])){
				dp[i][j] = 2;
				i--;
			}
			else {
				dp[i][j] = dp[j][k] + 1;
				max_len = max(max_len, dp[i][j]);
				if(max_len == dp[i][j]){
					ap_term = v[j] - v[i];
					ap_start = i;
				}
				i--;
				k++;
			}
		}
		while(i >= 0){
			dp[i][j] = 2;
			i--;
		}
	}
	cout << "max_len is: " << max_len << endl;
	cout << v[ap_start] << " ";
	for(int i=ap_start+1; i<n; i++){
		if((v[ap_start] - v[i])%ap_term == 0)
			cout << v[i] <<  " ";
	}
	cout << endl;	
	
	for(int i=0; i<n; i++){
		for(int j=0; j<n; j++){
			cout << dp[i][j] << " ";
		}
		cout << endl;
	}
	cout << endl;
}
 
	
int main(){
	int n;
	cin >> n;
	vector<int> v(n);
	for(int i=0; i<n; i++) cin >> v[i];
	llap(v);
	return 0;
}