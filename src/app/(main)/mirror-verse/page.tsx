
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Search } from 'lucide-react';

const relatedVerses = [
  { reference: 'Isaiah 53:5', text: 'But he was wounded for our transgressions, he was bruised for our iniquities...', match: 'Typology: Atonement' },
  { reference: 'Moses 1:39', text: 'For behold, this is my work and my glory—to bring to pass the immortality and eternal life of man.', match: 'Keyword: eternal life' },
  { reference: '2 Nephi 2:25', text: 'Adam fell that men might be; and men are, that they might have joy.', match: 'Keyword: joy' },
];

export default function MirrorVersePage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl md:text-4xl font-bold font-headline">Mirro-Verse</h1>
        <p className="text-lg text-muted-foreground">
          Discover related verses based on typology, themes, and keywords.
        </p>
      </div>

      <Card className="shadow-lg">
        <CardHeader>
          <CardTitle className="font-headline">Search Parameters</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="verse-input">Original Verse</Label>
              <Input id="verse-input" placeholder="e.g., John 3:16" defaultValue="John 3:16" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="typology-select">Typology</Label>
              <Select>
                <SelectTrigger id="typology-select">
                  <SelectValue placeholder="Select typology" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="atonement">Atonement</SelectItem>
                  <SelectItem value="covenant">Covenant</SelectItem>
                  <SelectItem value="sacrifice">Sacrifice</SelectItem>
                  <SelectItem value="creation">Creation</SelectItem>
                </SelectContent>
              </Select>
            </div>
             <div className="space-y-2">
              <Label htmlFor="keyword-input">Keywords</Label>
              <Input id="keyword-input" placeholder="e.g., love, faith" />
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button>
            <Search className="mr-2 h-4 w-4" />
            Find Mirro-Verses
          </Button>
        </CardFooter>
      </Card>
      
      <div className="space-y-4">
         <h2 className="text-2xl font-bold font-headline">Results</h2>
         <div className="grid gap-6">
            {relatedVerses.map((verse) => (
                <Card key={verse.reference} className="shadow-sm">
                    <CardHeader>
                        <CardTitle className="font-headline">{verse.reference}</CardTitle>
                        <CardDescription>Matched on: {verse.match}</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <p className="italic">"{verse.text}"</p>
                    </CardContent>
                </Card>
            ))}
         </div>
      </div>
    </div>
  );
}
