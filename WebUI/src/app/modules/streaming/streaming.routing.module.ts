import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StreamingContainer } from './components/streaming-container/streaming-container.component';

const routes: Routes = [
  {
    path: '',
    component: StreamingContainer,
  },
];

@NgModule({
  imports: [[RouterModule.forChild(routes)]],
  exports: [RouterModule],
})
export class StreamingRoutingModule {}
