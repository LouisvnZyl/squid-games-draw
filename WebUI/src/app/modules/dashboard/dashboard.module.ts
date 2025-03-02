import { NgModule } from '@angular/core';
import { BaseDashboardComponent } from './components/base-dashboard/base-dashboard.component';
import { DashboardRoutingModule } from './dashboard.routing.module';

@NgModule({
  imports: [DashboardRoutingModule, BaseDashboardComponent],
})
export class DashboardModule {}
