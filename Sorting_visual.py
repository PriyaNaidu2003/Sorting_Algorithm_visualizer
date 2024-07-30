import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from matplotlib.widgets import Button
# Generate random bars
num_bars = 25
bars = [random.randint(10, 100) for _ in range(num_bars)]


# Bubble Sort
def bubble_sort(bars):
    n = len(bars)
    for i in range(n):
        for j in range(0, n - i - 1):
            if bars[j] > bars[j + 1]:
                bars[j], bars[j + 1] = bars[j + 1], bars[j]
            yield bars, [j, j + 1]


# Insertion Sort
def insertion_sort(bars):
    for i in range(1, len(bars)):
        key = bars[i]
        j = i - 1
        while j >= 0 and key < bars[j]:
            bars[j + 1] = bars[j]
            j -= 1
            yield bars, [j + 1, j + 2]
        bars[j + 1] = key
        yield bars, [i, j + 1]


# Selection Sort
def selection_sort(bars):
    for i in range(len(bars)):
        min_idx = i
        for j in range(i + 1, len(bars)):
            if bars[min_idx] > bars[j]:
                min_idx = j
            yield bars, [i, j]
        bars[i], bars[min_idx] = bars[min_idx], bars[i]
        yield bars, [i, min_idx]


# Merge Sort
def merge_sort(bars, start, end):
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(bars, start, mid)
        yield from merge_sort(bars, mid, end)
        left = bars[start:mid]
        right = bars[mid:end]
        k = start
        i = 0
        j = 0
        while (start + i < mid) and (mid + j < end):
            if left[i] <= right[j]:
                bars[k] = left[i]
                i = i + 1
            else:
                bars[k] = right[j]
                j = j + 1
            k = k + 1
            yield bars, [start + i - 1, mid + j - 1]
        while start + i < mid:
            bars[k] = left[i]
            i = i + 1
            k = k + 1
            yield bars, [start + i - 1, mid + j - 1]
        while mid + j < end:
            bars[k] = right[j]
            j = j + 1
            k = k + 1
            yield bars, [start + i - 1, mid + j - 1]


def merge_sort_wrapper(bars):
    yield from merge_sort(bars, 0, len(bars))


# Quick Sort
def quick_sort(bars, start, end):
    if start >= end:
        return
    pivot = bars[end]
    pivot_idx = start
    for i in range(start, end):
        if bars[i] < pivot:
            bars[i], bars[pivot_idx] = bars[pivot_idx], bars[i]
            pivot_idx += 1
        yield bars, [i, pivot_idx]
    bars[end], bars[pivot_idx] = bars[pivot_idx], bars[end]
    yield bars, [pivot_idx, end]
    yield from quick_sort(bars, start, pivot_idx - 1)
    yield from quick_sort(bars, pivot_idx + 1, end)


def quick_sort_wrapper(bars):
    yield from quick_sort(bars, 0, len(bars) - 1)


# Function to update the bars
def update_bars(frame, rects, texts):
    bars, indices = frame
    for rect, val, text in zip(rects, bars, texts):
        rect.set_height(val)
        rect.set_color('blue')
        text.set_text(val)
        text.set_y(val + 1)  # Position the text just above the bar
        text.set_color('white')
    for index in indices:
        rects[index].set_color('red')
is_paused = False

def toggle_pause(event):
    global is_paused
    if is_paused:
        anim.event_source.start()
    else:
        anim.event_source.stop()
    is_paused = not is_paused

# Function to animate the sorting
def animate_sorting(sort_func, bars):
    global anim
    fig, ax = plt.subplots()
    rects = ax.bar(range(len(bars)), bars, align="edge")
    texts = [ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 1, rect.get_height(),
                     ha='center', va='bottom', color='blue') for rect in rects]

    ax.set_xlim(0, len(bars))
    ax.set_ylim(0, int(1.1 * max(bars)))

    # Change the background color here
    ax.set_facecolor('black')

    # Add a pause button
    axpause = plt.axes([0.85, 0.9, 0.1, 0.075])
    bpause = Button(axpause, 'Pause')
    bpause.on_clicked(toggle_pause)

    anim = animation.FuncAnimation(
        fig, update_bars, fargs=(rects, texts), frames=sort_func(bars), interval=300, repeat=False
    )
    plt.show()

# Main function
if __name__ == "__main__":
    choice = input("Choose sorting algorithm: (b)ubble, (i)nsertion, (s)election, (m)erge, (q)uick: ").lower()
    if choice == 'b':
        animate_sorting(bubble_sort, bars)
    elif choice == 'i':
        animate_sorting(insertion_sort, bars)
    elif choice == 's':
        animate_sorting(selection_sort, bars)
    elif choice == 'm':
        animate_sorting(merge_sort_wrapper, bars)
    elif choice == 'q':
        animate_sorting(quick_sort_wrapper, bars)
    else:
        print("Invalid choice.")
