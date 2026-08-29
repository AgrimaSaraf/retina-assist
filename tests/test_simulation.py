from simulation.clinic_generator import generate_clinic_cohort
from simulation.human_ai_generator import generate_human_ai_study
def test_clinic():
    v,a=generate_clinic_cohort(100,1); assert len(v)==100 and v.synthetic.eq(1).all() and a.synthetic.eq(1).all()
def test_hci():
    d=generate_human_ai_study(120,1); assert len(d)==120 and d.synthetic.eq(1).all()
