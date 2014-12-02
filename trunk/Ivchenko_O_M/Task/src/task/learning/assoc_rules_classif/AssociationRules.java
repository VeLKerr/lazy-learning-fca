package task.learning.assoc_rules_classif;

import task.learning.Acceptability;
import task.learning.Classificator;

/**
 *
 * @author VeLKerr
 */
public abstract class AssociationRules {
    public static final int COEFS_CNT = 4;
    protected double lim;
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
                return cnt;
            }
            default:{
                return power;
            }
        }
    }
}
