
package task.evaluating;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import task.learning.Acceptability;
import task.utils.Utils;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public abstract class Metrics<E extends Enum<E>>{
    protected abstract void takeIntoAccount(Acceptability actuals, Acceptability expected);
    
    protected abstract EnumMap<E, Double> countMetrics();
    
    protected abstract String headerToString();
    
    protected abstract String toString(boolean withHeader);
}
