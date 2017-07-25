def main():
    nums = [3,1,3,3,3]
    val = 3
    start, end = 0, len(nums) - 1
    while start <= end:
        if nums[start] == val:
            nums[start], nums[end], end = nums[end], nums[start], end - 1
        else:
            start += 1
        print start,end,nums
    # print nums
    return start
if __name__ == "__main__":
    num = main()
    print num