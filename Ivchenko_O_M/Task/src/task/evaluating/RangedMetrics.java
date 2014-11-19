
package task.evaluating;

import java.util.ArrayList;
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
public class RangedMetrics extends Metrics<RangedMetrics.Types>{
    private static final int DELIMITER = 1;
    private enum LabelTypes {
        TruePositive, 
        FalseNegative, 
        FalsePositive,
        TrueNegative
    };
    protected enum Types{
        ACCURACY(true) {
            @Override
            protected String getShortName(){
                return "Accur.";
            }
        },
        PRECISION(true) {
            @Override
            protected String getShortName(){
                return "Prec.";
            }
        },
        RECALL(true) {
            @Override
            protected String getShortName() {
                return "Recall";
            }
        },
        F_MEASURE(true) {
            @Override
            protected String getShortName() {
                return "F1";
            }
        },
        NEGATIVE_PRECISION(false) {
            @Override
            protected String getShortName() {
                return "N.Prec.";
            }
        },
        SPECIFYCITY(false) {
            @Override
            protected String getShortName() {
                return "Spec.";
            }
        },
        SENSITIVITY(false) {
            @Override
            protected String getShortName() {
                return "Sens.";
            }
        },
        FALSE_DISCOVERY_RATE(false) {
            @Override
            protected String getShortName() {
                return "FDR.";
            }
        },
        FALSE_POSITIVE_RATE(false) {
            @Override
            protected String getShortName() {
                return "FPR.";
            }
        },
        ALPHA_ERROR(true) {
            @Override
            protected String getShortName() {
                return "a-err";
            }
        },
        BETA_ERROR(true) {
            @Override
            protected String getShortName() {
                return "b-err";
            }
        },
        MATTHEW(true) {
            @Override
            protected String getShortName() {
                return "Matthew";
            }
        };
        
        private final boolean isVisible;
        
        private Types(boolean visibility){
            this.isVisible = visibility;
        }
        
        protected abstract String getShortName();
        
        public static String getNamesToString(){
            StringBuilder sb = new StringBuilder();
            for(Types mnt: Types.values()){
                if(mnt.isVisible){
                    sb.append(mnt.getShortName()).append("\t");
                }
            }
            sb.append("\n");
            return sb.toString();
        }
    }
    
    /**
     * 0. TP,
     * 1. FN,
     * 2. FP,
     * 3. TN.
     */
    private final double[] cnts; //double, чтоб потом рассчитать среднее
    
    public RangedMetrics(){
        this.cnts = new double[LabelTypes.values().length];
        Arrays.fill(cnts, 0.1); //0,1 - чтоб не было NaN. В принципе, этот трюк
        //аналогичен смещению Лапласса
    }
    
    @Override
    protected EnumMap<Types, Double> countMetrics(){
        double sum = Utils.sum(cnts);
        return null; //TODO: Metrics
    }
    
    @Override
    public void takeIntoAccount(Acceptability actuals, Acceptability expected){
        LabelTypes lt = LabelTypes.TruePositive;
        if(expected.ordinal() < DELIMITER && actuals.ordinal() < DELIMITER){
            lt = LabelTypes.TrueNegative;
        }
        else if(expected.ordinal() < DELIMITER && actuals.ordinal() >= DELIMITER){
            lt = LabelTypes.FalsePositive;
        }
        else if(expected.ordinal() >= DELIMITER && actuals.ordinal() < DELIMITER){
            lt = LabelTypes.FalseNegative;
        }
        cnts[lt.ordinal()] += 1;
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
            if(entry.getKey().isVisible){
                sb.append(Utils.roundDouble(entry.getValue())).append("\t");
            }
        }
        sb.append("\n");
        return sb.toString();
    }
    
    public static RangedMetrics avg(List<RangedMetrics> rangedMetricses){
        RangedMetrics res = new RangedMetrics();
        for(RangedMetrics rangedMetrics: rangedMetricses){
            for(int i=0; i<res.cnts.length; i++){
                res.cnts[i] += rangedMetrics.cnts[i];
            }
        }
        for(int i=0; i<res.cnts.length; i++){
            res.cnts[i] /= rangedMetricses.size();
        }
        return res;
    }
    
    public static String listToString(List<RangedMetrics> rangedMetricses){
        StringBuilder sb = new StringBuilder(Types.getNamesToString());
        for(RangedMetrics rangedMetrics: rangedMetricses){
            sb.append(rangedMetrics.toString(false));
        }
        return sb.toString();
    }
}
