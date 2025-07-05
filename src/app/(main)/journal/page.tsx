import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
} from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { CovenantEmber } from '@/components/app/covenant-ember';
import { Separator } from '@/components/ui/separator';

export default function JournalPage() {
  // Dummy data for demonstration
  const verseForJournaling = "Alma 32:21";
  const userJournalEntries = `Today I was thinking about faith. It's hard sometimes when you can't see the results. The idea of an experiment on the word is interesting. I tried to be more patient with my kids, even when it was difficult. I felt a small sense of peace afterward. Maybe that's the seed swelling.`;

  return (
    <div className="space-y-8">
       <div>
        <h1 className="text-3xl md:text-4xl font-bold font-headline">Fulfillment Journal</h1>
        <p className="text-lg text-muted-foreground">
          Log spiritual experiences and reflect on covenant fulfillment.
        </p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-2 shadow-lg">
          <CardHeader>
            <CardTitle className="font-headline text-2xl">New Journal Entry</CardTitle>
            <CardDescription>
              Record your thoughts and experiences related to the scriptures.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid w-full gap-4">
               <div className="flex flex-col space-y-2">
                <Label htmlFor="journal-entry">Your Reflections</Label>
                <Textarea id="journal-entry" placeholder="Write about your experiences, feelings, and insights..." className="min-h-[250px]" />
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex justify-end">
             <Button>Save Entry</Button>
          </CardFooter>
        </Card>

        <Card className="lg:col-span-1 shadow-lg">
           <CardHeader>
            <CardTitle className="font-headline text-2xl">Grace Buffer</CardTitle>
            <CardDescription>
              AI-powered prompts for deeper reflection.
            </CardDescription>
          </CardHeader>
          <CardContent>
             <CovenantEmber verse={verseForJournaling} journalEntries={userJournalEntries} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
