import java.util.*;

class Solution {
    public int minimumPairRemoval(int[] nums) {
        ArrayList<Long> a = new ArrayList<>(nums.length);
        for (int x : nums) a.add((long) x);

        int ops = 0;
        while (!isNonDecreasing(a)) {
            int idx = 0;
            long best = a.get(0) + a.get(1);

            // find adjacent pair with minimum sum (tie -> leftmost)
            for (int i = 1; i < a.size() - 1; i++) {
                long s = a.get(i) + a.get(i + 1);
                if (s < best) {
                    best = s;
                    idx = i;
                }
            }

            // replace pair (idx, idx+1) with their sum
            a.set(idx, best);
            a.remove(idx + 1);

            ops++;
        }
        return ops;
    }

    private boolean isNonDecreasing(ArrayList<Long> a) {
        for (int i = 1; i < a.size(); i++) {
            if (a.get(i) < a.get(i - 1)) return false;
        }
        return true;
    }
}