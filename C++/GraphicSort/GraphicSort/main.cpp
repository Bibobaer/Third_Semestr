#include "raylib.h"
#include <vector>
#include <iostream>
#include <time.h>

#define SCREEEN_WIDTH	1024
#define SCREEN_HEIGHT	720

void Print_Array(std::vector<int>& arr) {
    BeginDrawing();
    ClearBackground(RAYWHITE);
    for (int k = 0; k < arr.size(); k++) {
        DrawRectangle(k * (GetScreenWidth() / arr.size()), GetScreenHeight() - arr[k], (GetScreenWidth() / arr.size()) - 1, arr[k], BLUE);
    }
    EndDrawing();
    WaitTime(0.01);
}

void QuickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                std::swap(arr[i], arr[j]);
            }

            Print_Array(arr);
        }
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        Print_Array(arr);

        int pi = i + 1;
        QuickSort(arr, low, pi - 1);
        QuickSort(arr, pi + 1, high);
    }
}

int main(void) {
    InitWindow(SCREEEN_WIDTH, SCREEN_HEIGHT, "Visual Sorting");
    srand(time(0));

    std::vector<int> arr;

    for (int i = 0; i < 51; i++)
        arr.push_back(rand() % 500);

    while (!WindowShouldClose()) {
        QuickSort(arr, 0, arr.size() - 1);
    }

    CloseWindow();
    return 0;
}

