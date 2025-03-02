import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BaseDashboardComponent } from './components/base-dashboard/base-dashboard.component';

const routes: Routes = [
  {
    path: '',
    component: BaseDashboardComponent,
  },
];

@NgModule({
  imports: [[RouterModule.forChild(routes)]],
  exports: [RouterModule],
})
export class DashboardRoutingModule {}
