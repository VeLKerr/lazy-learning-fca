
package task.learning.assoc_rules_classif;

import task.learning.Acceptability;
import task.learning.Classificator;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public interface AssociationRules {
    public static final int COEFS_CNT = 4;
    
    public void takeIntoAccount(Classificator cl, Acceptability ac);
    
    public double getCoef(int coefImportanceCnt);
}
