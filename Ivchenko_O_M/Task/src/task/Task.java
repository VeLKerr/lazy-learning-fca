package task;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;
import java.util.Random;
import java.util.Set;
import task.crossvalidation.DataSplitter;
import task.evaluating.RankedMetrics;
import task.evaluating.UnrankedMetrics;
import task.learning.Acceptability;
import task.learning.Classificator;
import task.learning.Element;
import task.learning.assoc_rules_classif.AssociationRules;
import task.learning.assoc_rules_classif.AssociationRulesOnCnt;
import task.learning.assoc_rules_classif.AssociationRulesOnExtremums;
import task.utils.Utils;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class Task {
    public static abstract class Consts{
        public static final Random RANDOM = new Random(System.currentTimeMillis());
        public static final int SYMBOLS_AFTER_COMMA = 3;
        public static final String INPUT = "../../data_sets/cars/car.data";
        public static final int SIZE = 1728;
        public static final String DELIMITER = ",";
        public static final int CROSSVAL_CNT = 10;
    }
    
    private static Acceptability classificationImplic(Set<Classificator> classificators){
        EnumMap<Acceptability, Integer> implications = new EnumMap(Acceptability.class);
        Utils.initEnumMap(implications, 0);
        for(Classificator cl: classificators){
            if(cl.isImplication()){
                implications.put(cl.getImplicationGoal(), implications.get(cl.getImplicationGoal()) + 1);
            }
        }
        int max = 0;
        Acceptability result = null;
        for(Entry<Acceptability, Integer> entry: implications.entrySet()){
            if(entry.getValue() > max){
                max = entry.getValue();
                result = entry.getKey();
            }
        }
        return result;
    }
    
    public static <K extends AssociationRules> Acceptability weightedCalssif(EnumMap<Acceptability, K> map){
        double max = -Double.MAX_VALUE;
        //считаем максимальный вес
        for(Entry<Acceptability, K> entry: map.entrySet()){
            double localVal = entry.getValue().getWeightedValue();
            if(localVal > max){
                max = localVal;
            }
        }
        //оставляем только те значения ЦП, у которых вес равен максимальному 
        for(Entry<Acceptability, K> entry: map.entrySet()){
            if(entry.getValue().getWeightedValue() < max){
                map.remove(entry.getKey());
            }
        }
        //Из оставшихся случайно выбираем ответ
        Acceptability result = null;
        if(map.size() == 1){
            return map.keySet().iterator().next();
        }
        else if(!map.isEmpty()){
            int number = Consts.RANDOM.nextInt(map.size());
            int i = 0;
            Iterator<Acceptability> it = map.keySet().iterator();
            while(it.hasNext() && i < number){
                result = it.next();
                i++;
            }
        }
        return result;
    }
    
    public static Acceptability weightedCalssifCnt(EnumMap<Acceptability, AssociationRulesOnCnt> map){
        double max = -Double.MAX_VALUE;
        //считаем максимальный вес
        for(Entry<Acceptability, AssociationRulesOnCnt> entry: map.entrySet()){
            double localVal = entry.getValue().getWeightedValue();
            if(localVal > max){
                max = localVal;
            }
        }
        //оставляем только те значения ЦП, у которых вес равен максимальному 
        for(Entry<Acceptability, AssociationRulesOnCnt> entry: map.entrySet()){
            if(entry.getValue().getWeightedValue() < max){
                map.remove(entry.getKey());
            }
        }
        //Из оставшихся случайно выбираем ответ
        Acceptability result = null;
        if(map.size() == 1){
            return map.keySet().iterator().next();
        }
        else if(!map.isEmpty()){
            int number = Consts.RANDOM.nextInt(map.size());
            int i = 0;
            Iterator<Acceptability> it = map.keySet().iterator();
            while(it.hasNext() && i < number){
                result = it.next();
                i++;
            }
        }
        return result;
    }
    
    private static Acceptability classificationOnExtr(Set<Classificator> classificators, boolean isWeighted){
        Acceptability result = classificationImplic(classificators);
        if(result != null){
            return result;
        }
        //если не нашли ни одной импликации
        EnumMap<Acceptability, AssociationRulesOnExtremums> assocRules = new EnumMap(Acceptability.class);
        Utils.initEnumMap(assocRules, new AssociationRulesOnExtremums());
        //считаем максимальные коэффициенты по ассоциативным правилам
        for(Classificator cl: classificators){
            if(!cl.isImplication()){
                for(Entry<Acceptability, AssociationRulesOnExtremums> entry: assocRules.entrySet()){
                    entry.getValue().takeIntoAccount(cl, entry.getKey());
                }
            }
        }
        if(isWeighted){
            return weightedCalssif(assocRules);
        }
        /*Сравниваем сначала по достоверности. Если макс. достоверность правил 
        для какого-то значения целевого признака оказалась наибольшей, это значение
        признака и будет результатом. Если таких наибольших несколько, сравниваем
        ещё и по макс. поддержке.
        Если значений целевого признака снова получилось несколько, сравниваем их 
        по мин. мощности ассоц. правил. Далее - просто по количеству.
        */
        for(int i = 0; i<AssociationRules.COEFS_CNT; i++){
            double maxCoef = 0.0;
            for(Entry<Acceptability, AssociationRulesOnExtremums> entry: assocRules.entrySet()){
                if(entry.getValue().getCoef(i) > maxCoef){
                    maxCoef = entry.getValue().getCoef(i);
                }
            }
            for(Entry<Acceptability, AssociationRulesOnExtremums> entry: assocRules.entrySet()){
                if(entry.getValue().getCoef(i) != maxCoef){
                    assocRules.remove(entry.getKey());
                }
            }
            if(assocRules.size() == 1){
                assocRules.keySet().iterator().next();
            }
        }
        if(assocRules.size() != 1){
            int index = Consts.RANDOM.nextInt(assocRules.size());
            int ind = 0;
            Iterator<Acceptability> it = assocRules.keySet().iterator();
            while(it.hasNext() && ind <= index){
                result = it.next();
                ind++;
            }
        }
        return result;
    }
    
    private static Acceptability classificationOnCnt(Set<Classificator> classificators, double confLim, double suppLim, boolean isWeighted){
        Acceptability result = classificationImplic(classificators);
        if(result != null){
            return result;
        }
        //если не нашли ни одной импликации
        EnumMap<Acceptability, AssociationRulesOnCnt> assocRules = new EnumMap(Acceptability.class);
        Utils.initEnumMap(assocRules, new AssociationRulesOnCnt(confLim, suppLim));
        //считаем максимальные коэффициенты по ассоциативным правилам
        for(Classificator cl: classificators){
            if(!cl.isImplication()){
                for(Entry<Acceptability, AssociationRulesOnCnt> entry: assocRules.entrySet()){
                    entry.getValue().takeIntoAccount(cl, entry.getKey());
                }
            }
        }
        if(isWeighted){
            double max = -Double.MAX_VALUE;
            //считаем максимальный вес
            for(Entry<Acceptability, AssociationRulesOnCnt> entry: assocRules.entrySet()){
                double localVal = entry.getValue().getWeightedValue();
                if(localVal > max){
                    max = localVal;
                }
            }
            //оставляем только те значения ЦП, у которых вес равен максимальному 
            for(Entry<Acceptability, AssociationRulesOnCnt> entry: assocRules.entrySet()){
                if(entry.getValue().getWeightedValue() < max){
                    assocRules.remove(entry.getKey());
                }
            }
            //Из оставшихся случайно выбираем ответ
            if(assocRules.size() == 1){
                return assocRules.keySet().iterator().next();
            }
            else{
                int number = Consts.RANDOM.nextInt(assocRules.size());
                int i = 0;
                Iterator<Acceptability> it = assocRules.keySet().iterator();
                while(it.hasNext() && i < number){
                    result = it.next();
                    i++;
                }
            }
        }
        for(int i = 0; i<AssociationRules.COEFS_CNT; i++){
            double maxCoef = 0.0;
            for(Entry<Acceptability, AssociationRulesOnCnt> entry: assocRules.entrySet()){
                if(entry.getValue().getCoef(i) > maxCoef){
                    maxCoef = entry.getValue().getCoef(i);
                }
            }
            for(Entry<Acceptability, AssociationRulesOnCnt> entry: assocRules.entrySet()){
                if(entry.getValue().getCoef(i) != maxCoef){
                    assocRules.remove(entry.getKey());
                }
            }
            if(assocRules.size() == 1){
                assocRules.keySet().iterator().next();
            }
        }
        if(assocRules.size() != 1){
            int index = Consts.RANDOM.nextInt(assocRules.size());
            int ind = 0;
            Iterator<Acceptability> it = assocRules.keySet().iterator();
            while(it.hasNext() && ind <= index){
                result = it.next();
                ind++;
            }
        }
        return result;
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        List<Element> elements = new ArrayList<>();
        List<UnrankedMetrics> unrangedMetricses = new ArrayList<>();
        List<RankedMetrics> rangedMetricses = new ArrayList<>();
        for(int i=0; i<Consts.CROSSVAL_CNT; i++){
            UnrankedMetrics unrangedMetrics = new UnrankedMetrics();
            RankedMetrics rangedMetrics = new RankedMetrics();
            int[] testIndexes = DataSplitter.getInstance().generateIndexes();
            //System.out.println(testIndexes[0] + " " + testIndexes[1]);
            int elementCnt = 0;
            try(RandomAccessFile rsf = new RandomAccessFile(Consts.INPUT, "r")){
                String line = null;
                //обучение
                while((line = rsf.readLine()) != null){
                    if(elementCnt <= testIndexes[0] || elementCnt > testIndexes[1]){
                        elements.add(new Element(line));
                    }
                    elementCnt++;
                }
                elementCnt = 0;
                rsf.seek(0);
                //тестировка
                Classificator.setTrainingDataSize(elements.size());
                while((line = rsf.readLine()) != null){
                    if(elementCnt > testIndexes[0] && elementCnt <= testIndexes[1]){
                        Element newEl = new Element(line);
                        //построение классификаторов
                        Set<Classificator> classificators = new HashSet<>();
                        for(Element el: elements){
                            Classificator cl = newEl.intersect(el);
                            for(Element e: elements){
                                if(!e.equals(el)){
                                    cl.add(e.contains(cl));
                                }
                            }
                            if(!cl.isEmpty()){
                                classificators.add(cl);
                            }
                        }
                        //классификация
                        Acceptability classificationRes = classificationOnCnt(classificators, 1, 1, true);
                        //Acceptability classificationRes = classificationOnExtr(classificators, true);
                        //оценка алгоритма
                        unrangedMetrics.takeIntoAccount(classificationRes, newEl.getAcceptability());
                        rangedMetrics.takeIntoAccount(classificationRes, newEl.getAcceptability());
                        //дообучение
                        elements.add(newEl);
                    }
                    elementCnt++;
                }
                elements.clear();
                unrangedMetricses.add(unrangedMetrics);
                rangedMetricses.add(rangedMetrics);
            }
            catch(IOException ex){
                System.err.println("Unable to read the file!" + elementCnt);
            }
        }
        System.out.println(UnrankedMetrics.listToString(unrangedMetricses));
        Utils.avgConsole(10, 15);
        System.out.println(UnrankedMetrics.avg(unrangedMetricses).toString(false));
        
        RankedMetrics avgRM = RankedMetrics.avg(rangedMetricses);
        System.out.println(RankedMetrics.listToString(rangedMetricses, true));
        Utils.avgConsole(10, 15);
        System.out.println(avgRM.basicNoRangedToString(false));
        System.out.println(RankedMetrics.listToString(rangedMetricses, false));
        Utils.avgConsole(10, 15);
        System.out.println(avgRM.toString(false));
    }
}