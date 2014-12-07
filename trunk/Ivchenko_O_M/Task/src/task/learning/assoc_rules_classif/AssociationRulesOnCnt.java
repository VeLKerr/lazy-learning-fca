
package task.learning.assoc_rules_classif;

import task.learning.Acceptability;
import task.learning.Classificator;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class AssociationRulesOnCnt extends AssociationRules{

    public AssociationRulesOnCnt(double confLim, double suppLim) {
        this.power = 0;
        this.confidence = 0.0;
        this.support = 0.0;
        this.cnt = 0;
        this.confLim = confLim;
        this.suppLim = suppLim;
    }
    
    @Override
    public void takeIntoAccount(Classificator cl, Acceptability ac){
        double conf = cl.getConfidence(ac);
        double supp = cl.getSupport(ac);
        if(conf >= confLim && supp >= suppLim){
            power += cl.getPower();
            support += supp;
            confidence += conf;
            cnt++;
        }
    }
}
