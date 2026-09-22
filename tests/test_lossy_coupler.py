import numpy as np
from analysis.s0c_coupler_feasibility import lossy_section


def test_feedback_against_independent_linear_system_and_passivity():
    for k in [.05,.3282,.95]:
        for loss in [0,.1,.67]:
            s=10**(-loss/20)
            S=s*np.array([[np.sqrt(1-k),1j*np.sqrt(k)],[1j*np.sqrt(k),np.sqrt(1-k)]])
            for angle in np.linspace(-np.pi,np.pi,19):
                q=.999*np.exp(1j*angle)
                # Solve y = S [1, q*y_ring], for both outgoing fields.
                A=np.eye(2,dtype=complex);A[:,1]-=S[:,1]*q
                y=np.linalg.solve(A,S[:,0])
                np.testing.assert_allclose(lossy_section(q,k,loss),y[0],atol=1e-13)
                assert abs(y[0])<=1+1e-12
                if loss==0:
                    t=np.sqrt(1-k)
                    np.testing.assert_allclose(y[0],(t-q)/(1-t*q),atol=1e-13)


def test_ideal_mzi_map_and_common_phase_compensation():
    # B diag(exp(i theta),1) B^H gives common phase and a symmetric coupler.
    B=np.array([[1,1j],[1j,1]])/np.sqrt(2)
    for theta in np.linspace(.1,3.,9):
        M=B@np.diag([np.exp(1j*theta),1])@B.conj().T
        np.testing.assert_allclose(abs(M[0,1])**2,np.sin(theta/2)**2,atol=1e-14)
        q=.999*np.exp(1j*(.7-theta/2))
        A=np.eye(2,dtype=complex);A[:,1]-=M[:,1]*q
        y=np.linalg.solve(A,M[:,0])[0]
        np.testing.assert_allclose(y*np.exp(-1j*theta/2),lossy_section(.999*np.exp(.7j),np.sin(theta/2)**2,0),atol=1e-13)
