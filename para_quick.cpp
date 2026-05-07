#include <iostream>
#include <vector>
#include <omp.h>
using namespace std;

// Partition function
int partition(vector<int> &arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

// Parallel quicksort using tasks
void quickSort(vector<int> &arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        #pragma omp task shared(arr)
        quickSort(arr, low, pi - 1);

        #pragma omp task shared(arr)
        quickSort(arr, pi + 1, high);
    }
}

int main() {
    int n;
    cout << "Enter number of elements: ";
    cin >> n;

    vector<int> arr(n);
    cout << "Enter elements:\n";
    for (int i = 0; i < n; i++) cin >> arr[i];

    cout << "\nOriginal array:\n";
    for (int x : arr) cout << x << " ";
    cout << endl;

    double start = omp_get_wtime();

    // Start parallel region
    #pragma omp parallel
    {
        #pragma omp single
        quickSort(arr, 0, n - 1);
    }

    double end = omp_get_wtime();

    cout << "\nSorted array:\n";
    for (int x : arr) cout << x << " ";
    cout << endl;

    cout << "\nExecution time: " << (end - start) << " seconds\n";

    return 0;
}


/*
g++ 4_parallel_quicksort.cpp -fopenmp -o quick
quick


Example Run:

Input:
Enter number of elements: 5
Enter elements:
5 4 3 2 1

Output:
Original array:
5 4 3 2 1

Sorted array:
1 2 3 4 5

Execution time: 0.0001 seconds

