import { NgModule } from '@angular/core';
import { StreamingRoutingModule } from './streaming.routing.module';
import { StreamingContainer } from './components/streaming-container/streaming-container.component';

@NgModule({
  imports: [StreamingRoutingModule, StreamingContainer],
})
export class StreamingModule {}
