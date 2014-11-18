
package task.learning.assoc_rules_classif;

import task.learning.Acceptability;
import task.learning.Classificator;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class AssociationRulesOnExtremums implements AssociationRules{
    private int power;
    private double confidence;
    private double support;
    private int cnt;
    
    public AssociationRulesOnExtremums() {
        this.power = Integer.MAX_VALUE;
        this.confidence = 0.0;
        this.support = 0.0;
        this.cnt = 0;
    }

    @Override
    public void takeIntoAccount(Classificator cl, Acceptability ac) {
        double conf = cl.getConfidence(ac);
        double supp = cl.getSupport(ac);
        if(conf != 0.0 && supp > 2){
            if(conf > confidence){
                confidence = conf;
            }
            if(supp > support){
                support = supp;
            }
            int pow = cl.getPower();
            if(pow < power){
                power = pow;
            }
            cnt++;
        }
    }

    @Override
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
