# computing z-stat
# hypo_mean = 4.8

# Xsample_mean = 4.1
# n = 25

def computing_z_proportion(HypothesisProportion, SampleProportion, n):
    p = HypothesisProportion
    q = 1 - HypothesisProportion
    pHat = SampleProportion
    z_stat = (pHat - p) / (p*q/n)**(0.5)
    print(z_stat)

def computing_z(Xsample_mean, hypo_mean, n):
    SDpopulation = float(input("Give population SD: "))
    z_stat_observe = (Xsample_mean - hypo_mean) / ( SDpopulation/(n)**(0.5) )
    print (z_stat_observe)

# t table http://www.dummies.com/education/math/statistics/how-to-use-the-t-table-to-solve-statistics-problems/
def computing_t(Xsample_mean, hypo_mean, n):
    SDsample = float(input("Give sample SD: "))
    t_stat_observe = (Xsample_mean - hypo_mean) / ( SDsample/((n)**(0.5)) )
    print (t_stat_observe)

def user_interface():
    user_input = input("What do you want to compute?\n(1:t | 2:z | 3:t_stat | 4:z_stat | 5: z_stat_proportion):")
    # t-stat
    if user_input == "3" or user_input == "t_stat":
        hypo_mean = float(input("Give hypothesis mean: "))
        Xsample_mean = float(input("Give sample mean: "))
        n = int(input("Give sample size: "))
        computing_t(Xsample_mean, hypo_mean, n)
    elif user_input == "4" or user_input == "z_stat":
        hypo_mean = float(input("Give hypothesis mean: "))
        Xsample_mean = float(input("Give sample mean: "))
        n = int(input("Give sample size: "))
        computing_z(Xsample_mean, hypo_mean, n)
    elif user_input == "5" or user_input == "z_stat_proportion":
        HypothesisProportion = float(input("Give Hypothesis i.e. population proportion: "))
        SampleProportion = float(input("Give sample proportion: "))
        n = int(input("Give sample size: "))
        computing_z_proportion(HypothesisProportion, SampleProportion, n)
    else:
        print("look up table no gonna compute for ya!")

user_interface()
