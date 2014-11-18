
package task.learning.assoc_rules_classif;

import task.learning.Acceptability;
import task.learning.Classificator;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class AssociationRulesOnCnt implements AssociationRules{
    private int power;
    private double confidence;
    private double support;
    private int cnt;

    public AssociationRulesOnCnt() {
        this.power = 0;
        this.confidence = 0.0;
        this.support = 0.0;
        this.cnt = 0;
    }
    
    @Override
    public void takeIntoAccount(Classificator cl, Acceptability ac){
        double conf = cl.getConfidence(ac);
        double supp = cl.getSupport(ac);
        if(conf != 0.0 && supp > 2){
            power += cl.getPower();
            support += supp;
            confidence += conf;
            cnt++;
        }
    }
    
    @Override
    public double getCoef(int coefImportanceCnt){
        switch(coefImportanceCnt){
            case 0:{
                return cnt;
            }
            case 1:{
                return confidence;
            }
            case 2:{
                return support;
            }
            default:{
                return power;
            }
        }
    }
}
