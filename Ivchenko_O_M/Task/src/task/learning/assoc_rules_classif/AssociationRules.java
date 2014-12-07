package task.learning.assoc_rules_classif;

import task.learning.Acceptability;
import task.learning.Classificator;

/**
 *
 * @author VeLKerr
 */
public abstract class AssociationRules {
    public static final int COEFS_CNT = 4;
    private static double[] weights = {10.8, 4.5, -1.9, 1.1};
    protected double confLim;
    protected double suppLim;
    protected int power;
    protected double confidence;
    protected double support;
    protected int cnt;
    
    public abstract void takeIntoAccount(Classificator cl, Acceptability ac);
    
    public double getCoef(int coefImportanceCnt) {
        switch(coefImportanceCnt){
            case 0:{
                return confidence;
            }
            case 1:{
                return support;
            }
            case 2:{
                return power;
            }
            default:{
                return cnt;
            }
        }
    }
    
    public double getWeightedValue(){
        double sum = 0;
        for(int i=0; i<weights.length; i++){
            sum += weights[i] * getCoef(i);
        }
        return sum;
    }
}
