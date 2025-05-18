import os
import ogstools as ot


class NUMMODEL():
    def __init__(self, _, project_name="./", ogsinputdir="/home/buchwalj/github/parameter_sampling/example/",
            ogs_mode="silent"):
        self.project_name = project_name
        self.ogs_mode = ogs_mode
        self.ogsinputdir = ogsinputdir

    def run(self, folder, prefix, data, distribution, time_run, time_out):

        self.filename = os.path.join(self.project_name, "results", folder, prefix + "_ogs.prj")
        self.prefix = os.path.join(self.project_name, "results", folder, prefix)
        self.model = ot.Project(input_file=os.path.join(self.ogsinputdir,"test.prj"), output_file=self.filename)
        self.identifier = prefix
        self.damping = data['damping']
        print(data["residual_gas_saturation"])
        self.residual_gas_saturation = data['residual_gas_saturation']
        self.write_input()
        self.run_model()

    def write_input(self):
        #self.model.replace_text(value=str(self.damping), xpath="./nonlinear_solvers/nonlinear_solver/damping")
        self.model.replace_text(value=str(self.residual_gas_saturation), xpath="./media/medium/properties/property[name='relative_permeability']/residual_gas_saturation")
        self.model.replace_text(value=str(self.residual_gas_saturation), xpath="./media/medium/properties/property[name='saturation']/residual_gas_saturation")
        self.model.write_input()
    def run_model(self):
        self.model.run_model(path="/home/buchwalj/github/ogs-build/RM_parallel_assembly/bin",
                             wrapper="source /opt/intel/oneapi/setvars.sh && export OMP_NUM_THREADS=6 && export OGS_ASM_THREADS=6 &&",
                             logfile=self.filename.replace(".prj", ".log"),
                             args=f"-m {self.ogsinputdir}/mesh -o {self.ogsinputdir}/out")
