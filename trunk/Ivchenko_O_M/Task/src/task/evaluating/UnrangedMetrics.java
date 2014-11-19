
package task.evaluating;

import java.util.Arrays;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import task.learning.Acceptability;
import task.utils.Utils;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class UnrangedMetrics extends Metrics<UnrangedMetrics.Types>{
    protected enum Types{
        MAE(true),
        RMSE(true),
        NMAE(false),
        NRMSE(false);
        
        private final boolean isAnotherSumCountMethod;
        
        private Types(boolean isAnotherSumCountMethod){
            this.isAnotherSumCountMethod = isAnotherSumCountMethod;
        }
        
        public static int relevamtMetricsCount(){
            int cnt = 0;
            for(Types t: values()){
                if(t.isAnotherSumCountMethod){
                    cnt++;
                }
            }
            return cnt;
        }
        
        public static String getNamesToString(){
            StringBuilder sb = new StringBuilder();
            for(Types t: values()){
                sb.append(t.name()).append("\t");
            }
            sb.append("\n");
            return sb.toString();
        }
    }
    
    private final double[] sums;
    private int cnt;
    
    public UnrangedMetrics(){
        this.cnt = 0;
        this.sums = new double[Types.relevamtMetricsCount()];
        Arrays.fill(sums, 0);
    }

    private UnrangedMetrics(double [] sums, int cnt) {
        this.sums = sums;
        this.cnt = cnt;
    }
    
    @Override
    public void takeIntoAccount(Acceptability actuals, Acceptability expected){
        int diff = actuals.ordinal() - expected.ordinal();
        sums[0] += Math.abs(diff);
        sums[1] += (int)Math.pow(diff, 2);
        cnt++;
    }
    
    @Override
    protected EnumMap<Types, Double> countMetrics(){
        EnumMap<Types, Double> map = new EnumMap(Types.class);
        double m1 = sums[0] / cnt;
        map.put(Types.MAE, m1);
        map.put(Types.NMAE, m1 / Acceptability.values().length);
        double m2 = Math.sqrt(sums[1] / cnt);
        map.put(Types.RMSE, m2);
        map.put(Types.NRMSE, m2 / Acceptability.values().length);
        return map;
    }
    
    @Override
    public String headerToString(){
        return Types.getNamesToString();  
    }
    
    @Override
    public String toString(boolean withHeader){
        StringBuilder sb = new StringBuilder();
        if(withHeader){
            sb.append(Types.getNamesToString());
        }
        EnumMap<Types, Double> metrics = countMetrics();
        for(Entry<Types, Double> entry: metrics.entrySet()){
            sb.append(Utils.roundDouble(entry.getValue())).append("\t");
        }
        sb.append("\n");
        return sb.toString();
    }
    
    public static UnrangedMetrics avg(List<UnrangedMetrics> unrangedMetricses){
        double[] sums = new double[Types.relevamtMetricsCount()]; //значения cnt у всех должны быть равны!
        for(UnrangedMetrics unrangedMetrics: unrangedMetricses){
            for(int i=0; i<sums.length; i++){
                sums[i] += unrangedMetrics.sums[i];
            }
        }
        for(int i=0; i<sums.length; i++){
            sums[i] /= unrangedMetricses.size();
        }
        return new UnrangedMetrics(sums, unrangedMetricses.get(0).cnt);
    }
    
    public static String listToString(List<UnrangedMetrics> unrangedMetricses){
        StringBuilder sb = new StringBuilder(Types.getNamesToString());
        for(UnrangedMetrics unrangedMetrics: unrangedMetricses){
            sb.append(unrangedMetrics.toString(false));
        }
        return sb.toString();
    }
}
