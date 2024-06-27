class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        max = 0
        counter = 0
        for i in nums:
            if nums[i] == 1:
                counter +=1
            else:
                if counter > max:
                    max = counter

        return max