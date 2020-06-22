import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FirstComponent } from './first/first.component';
import { SecondComponent } from './second/second.component';
import { ThirdComponent } from './third/third.component';
import { ImplementationComponent } from './implementation/implementation.component';

const routes: Routes = [
  { path: 'analysis', component: ThirdComponent },
  { path: '', component: FirstComponent },
  { path: 'logic', component: SecondComponent },
  { path: 'implementation', component: ImplementationComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
