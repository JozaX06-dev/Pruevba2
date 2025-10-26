# O(n log n) - Tiempo logarítmico (como mergesort)
def merge_sort(arr, key=None):
    
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    
    return merge(left, right, key)


def merge(left, right, key=None):
    
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Si hay función key, usarla para comparar
        if key:
            left_val = key(left[i])
            right_val = key(right[j])
        else:
            left_val = left[i]
            right_val = right[j]
        
        # Comparación case-insensitive si son strings
        if isinstance(left_val, str):
            left_val = left_val.lower()
            right_val = right_val.lower()
        
        if left_val < right_val:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result