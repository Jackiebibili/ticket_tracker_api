def percentile(num_before: int, total: int) -> float:
   denominator = total
   if denominator == 0:
      denominator = 1
   return num_before / denominator

def percentileInBetween(num_before: int, num_after: int)->float:
   denominator = num_before + num_after + 1
   return percentile(num_before, denominator)
