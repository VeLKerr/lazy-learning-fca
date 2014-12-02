
package task.learning.assoc_rules_classif;

import task.learning.Acceptability;
import task.learning.Classificator;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class AssociationRulesOnCnt extends AssociationRules{

    public AssociationRulesOnCnt(double lim) {
        this.power = 0;
        this.confidence = 0.0;
        this.support = 0.0;
        this.cnt = 0;
        this.lim = lim;
    }
    
    @Override
    public void takeIntoAccount(Classificator cl, Acceptability ac){
        double conf = cl.getConfidence(ac);
        if(conf >= lim){
            double supp = cl.getSupport(ac);
            if(supp > 2){
                power += cl.getPower();
                support += supp;
                confidence += conf;
                cnt++;
            }
        }
    }
}
