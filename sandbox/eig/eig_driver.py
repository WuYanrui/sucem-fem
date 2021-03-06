## Copyright (C) 2011 Stellenbosch University
##
## This file is part of SUCEM.
##
## SUCEM is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## SUCEM is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SUCEM. If not, see <http://www.gnu.org/licenses/>. 
##
## Contact: cemagga@gmail.com 
# Authors:
# Neilen Marais <nmarais@gmail.com>
from __future__ import division

import sys
sys.path.append('../../')
import numpy as N
import os
import dolfin as dol

from sucemfem.ProblemConfigurations.EMVectorWaveEigenproblem import EigenProblem
from sucemfem.ProblemConfigurations.EMVectorWaveEigenproblem import DefaultEigenSolver

from sucemfem.Consts import c0


# Define mesh
# mesh = dol.UnitCube(1,1,1)
# mesh.coordinates()[:] *= [cdims.a,cdims.b,cdims.c]
#mesh_file = 'lee_mittra92_fig6b.xml'
#mesh_file = 'lee_mittra92_fig6c.xml'
mesh_file = '../../examples/albani_bernardi74/mesh/albani_bernardi74_fig2VII.xml'
materials_mesh_file = "%s_physical_region%s" % (os.path.splitext(mesh_file))
mesh = dol.Mesh(mesh_file)
material_mesh_func = dol.MeshFunction('uint', mesh, materials_mesh_file)
materials = {1000:dict(eps_r=16),
             1001:dict(eps_r=1)}
order = 3
sigma = 1.5

# Set up eigen problem
ep = EigenProblem()
ep.set_mesh(mesh)
ep.set_basis_order(order)
ep.set_material_regions(materials)
ep.set_region_meshfunction(material_mesh_func)
ep.init_problem()

# Set up eigen problem linear solution
es = DefaultEigenSolver()
es.set_eigenproblem(ep)
es.set_sigma(sigma)
eigs_w, eigs_v = es.solve_problem(10)


res = N.array(sorted(eigs_w)[0:10])
print N.sqrt(res)
print c0*N.sqrt(res)/2/N.pi/1e6
#errs = postproc_eigres.calc_errs(res)
#postproc_eigres.print_errs(errs)


