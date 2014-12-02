
package task.learning.assoc_rules_classif;

import task.learning.Acceptability;
import task.learning.Classificator;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class AssociationRulesOnExtremums extends AssociationRules{
    
    public AssociationRulesOnExtremums() {
        this.power = Integer.MAX_VALUE;
        this.confidence = 0.0;
        this.support = 0.0;
        this.cnt = 0;
        this.lim = 0.0;
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
}
